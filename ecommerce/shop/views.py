from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, TemplateView

from .forms import UserLogForm, UserRegForm, Reviews
from .models import Category, Product, Review, ReviewImages, WishList, Cart, Orders, OrdersItem


# Create your views here.


class HomeView(ListView):
    """Домашняя Страница"""
    paginate_by = 16
    model = Product
    context_object_name = 'products'
    template_name = 'shop/main_page.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            object_list = Product.objects.filter(Q(name__icontains=query))
        else:
            object_list = Product.objects.all()
        return object_list


def detail_view(request, slug):
    context = {}
    # Получение Товара
    product = Product.objects.get(slug=slug)

    # Если пост, то записываем отзыв в модель
    if request.method == 'POST':
        if request.user.is_authenticated and not Review.objects.filter(username=request.user.id, product=product):
            rating = request.POST['rating']
            review = request.POST['feedback']

            user = User.objects.get(username=request.user.username)

            rev = Review(rating=rating, text=review, username=user, product=product)
            rev.save()

            # Проверка на наличие Отправленных Файлов

            if request.FILES:
                files = request.FILES.getlist('files')
                for file in files:
                    fs = FileSystemStorage()
                    # сохраняем на файловой системе
                    filename = fs.save(file.name, file)
                    ex = ReviewImages(img=filename, product=product, review=rev)
                    ex.save()

            return redirect('one_pr', slug=slug)
        else:
            messages.error(request, 'У вас Уже есть отзыв на данный товар')
    # Получение Отзывов на товар
    reviews = Review.objects.filter(product=product)
    img_reviews = ReviewImages.objects.filter(product=product)

    context['reviews'] = reviews
    context['img_reviews'] = img_reviews

    # Характеристики из модели в виде list[tuple(key, val)]
    good = product.characteristics
    goods_key = good.split(",")[::2]
    goods_val = good.split(",")[1::2]
    info = list(zip(goods_key, goods_val))
    context["info"] = info
    context['product'] = product

    # Укороченная инфо для Начального Отображения
    context['info_sm'] = info[:5]

    context['form'] = Reviews()

    # Средний Рейтинг Товара
    reviews = Review.objects.filter(product=product)
    if reviews:
        avg_rating = 0
        for review in reviews:
            avg_rating += review.rating
        avg = round(avg_rating / len(reviews), 1)
        product.avg_rating = avg
        product.save()

    return render(request, 'shop/detail_pr.html', context)


def prod_by_category(request, category):
    """Продукты упорядоченные по категории"""
    cat = Category.objects.get(category_name=category)
    products = Product.objects.filter(category=cat)
    return render(request, 'shop/base.html', context={
        'products': products,
    })


class UserLogView(LoginView):
    """Вход"""
    form_class = UserLogForm
    template_name = 'shop/registration/login_user.html'

    def get_success_url(self):
        return "/"


class UserRegView(CreateView):
    """Регистрация"""
    form_class = UserRegForm
    template_name = 'shop/registration/sign_up.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


def sign_out(request):
    """Выход"""
    logout(request)
    return redirect('/')


def add_to_wish_list(request):
    """Добавление в Избранное"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('product_id'))
            if WishList.objects.filter(
                    product=request.POST.get('product_id'), user=request.user.id):
                return JsonResponse(
                    {'status': 'Product Already added'})
            else:
                WishList.objects.create(user=request.user, product=product)
                return JsonResponse({'status': 'Successfully Added'})
        else:
            return JsonResponse({'status': 'Login to continue'})

    return redirect('/')


def delete_from_wish_list(request):
    """Удаление из Избранного"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        if product:
            WishList.objects.get(product=product).delete()
            return JsonResponse({'status': 'Successfully deleted'})
        else:
            return JsonResponse({'status': 'Product unavailable'})
    else:
        return redirect('/')


def wish_list(request):
    wish_products = WishList.objects.filter(user=request.user.id)
    return render(request, 'shop/wishlist.html', context={
        'wish_products': wish_products,
    })


def checkout(request):
    """Оплата"""
    if request.method == 'GET':
        cart_products = Cart.objects.filter(user=request.user.id)

        total = 0
        for item in cart_products:
            total += item.sub_total()

        return render(request, 'shop/payment/checkout.html', context={
            'cart_products': cart_products,
            'total': total,
        })

    if request.method == 'POST':
        total = 0
        cart_items = Cart.objects.filter(user=request.user)
        current_order = Orders.objects.create(user=request.user, status='В сборке у продавца')

        for cart_item in cart_items:
            # Манипуляции с CartItem
            total += cart_item.sub_total()
            cart_item.product.stock -= 1

            # Создание Item и его присоединение к order
            item = OrdersItem.objects.create(product=cart_item.product, quantity=cart_item.quantity)
            current_order.order_items.add(item)

            # Сохранение Кол-во продукта на складе и удаление корзины пользователя
            cart_item.product.save()
            cart_item.delete()

        current_order.total = total
        current_order.save()

        return redirect(reverse('checkout_success'))


class CheckFailed(TemplateView):
    template_name = 'shop/payment/checkout_failed.html'


class CheckSuccess(TemplateView):
    template_name = 'shop/payment/checkout_success.html'
