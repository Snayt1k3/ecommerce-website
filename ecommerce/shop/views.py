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
from .models import Category, Product, Review, ReviewImages, WishList, Cart, Orders, PersonalArea


# Create your views here.


class HomeView(ListView):
    """Домашняя Страница"""
    paginate_by = 16
    model = Product
    context_object_name = 'products'
    template_name = 'shop/base.html'

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
        if request.user.is_authenticated:
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


def cart(request):
    """Корзина"""
    user_cart = Cart.objects.filter(user=request.user.id)
    total = 0
    for item in user_cart:
        total += item.sub_total()

    return render(request, 'shop/cart.html', context={
        'user_cart': user_cart,
        'total': total,
    })


def add_to_cart(request):
    """Добавление Товара В Корзину"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('product_id'))
            if product:
                if Cart.objects.filter(product=product, user=request.user.id):
                    return JsonResponse({'status': 'Product Already added'})
                else:
                    Cart.objects.create(user=request.user, product=product)
                    return JsonResponse({'status': 'Successfully Added'})
            else:
                return JsonResponse({'status': 'Product unavailable'})
        else:
            return JsonResponse({'status': 'Login to continue'})
    else:
        return redirect('/')


def minus_quantity(request):
    """Уменьшение Кол-ва Товара в корзине"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        cart_item = Cart.objects.get(product=product, user=request.user.id)
        if cart_item.quantity == 1:
            cart_item.delete()
            return JsonResponse({'status': 'Successfully Deleted from cart'})
        else:
            cart_item.quantity -= 1
            cart_item.save()
            return JsonResponse({'status': 'Quantity Updated'})
    else:
        return redirect('/')


def plus_quantity(request):
    """Увеличение Кол-ва Товара в корзине"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        cart_item = Cart.objects.get(product=product, user=request.user.id)
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            return JsonResponse({'status': 'Quantity Updated'})
        else:
            return JsonResponse({'status': f'Product stock - {product.stock}'})
    else:
        return redirect('/')


def delete_from_cart(request):
    """Удаление Товара Из Корзины"""
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        cart_item = Cart.objects.get(product=product, user=request.user.id)
        cart_item.delete()
        return JsonResponse({'status': 'Successfully Deleted'})
    else:
        return redirect('/')


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
            total += cart_item.sub_total()
            current_order.products.add(cart_item.product)
            cart_item.product.stock -= 1
            cart_item.product.save()
            cart_item.delete()

        current_order.total = total
        current_order.save()

        return redirect(reverse('checkout_success'))


class CheckFailed(TemplateView):
    template_name = 'shop/payment/checkout_failed.html'


class CheckSuccess(TemplateView):
    template_name = 'shop/payment/checkout_success.html'


def profile_user_view(request, username):
    context = {}
    if not request.user.is_authenticated or request.user.username != username:
        return redirect('home')

    if not PersonalArea.objects.filter(user=request.user):
        PersonalArea.objects.create(user=request.user)

    more_info_user = PersonalArea.objects.get(user=request.user)
    history_orders = Orders.objects.filter(user=request.user, status='received')
    current_orders = Orders.objects.exclude(status='received').filter(user=request.user).order_by('id')

    context['more_info_user'] = more_info_user
    context['history_orders'] = history_orders
    context['current_orders'] = current_orders.reverse()

    return render(request, 'shop/profile_user.html', context)


def profile_user_edit_view(request, username):
    if not request.user.is_authenticated or request.user.username != username:
        return redirect('home')

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        avatar = request.FILES.get('avatar')

        user = User.objects.get(username=username)
        user_profile = PersonalArea.objects.get(user=user)

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if phone:
            user_profile.phone = phone

        if address:
            user_profile.address = address

        if avatar:
            fs = FileSystemStorage()
            # сохраняем на файловой системе
            filename = fs.save(avatar.name, avatar)
            user_profile.avatar = filename

        user.save()
        user_profile.save()

        return redirect('profile', username=username)
    else:
        user = User.objects.get(username=username)
        user_profile = PersonalArea.objects.get(user=user)
        return render(request, 'shop/profile_edit.html', context={
            'more_info_user': user_profile
        })
