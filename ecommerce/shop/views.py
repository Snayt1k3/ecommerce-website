from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView

from .forms import UserLogForm, UserRegForm, Reviews
from .models import Category, Product, Review, ReviewImages, WishList


# Create your views here.


class HomeView(ListView):
    """Домашняя Страница"""
    paginate_by = 16
    model = Product
    context_object_name = 'products'
    template_name = 'shop/base.html'


def detail_view(request, slug):
    context = {'user_not_auth': False}
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
        else:
            context['user_not_auth'] = True

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
    context['info_sm'] = info[:6]

    context['form'] = Reviews()
    return render(request, 'shop/detail_pr.html', context)


def prod_by_category(request, category):
    """Продукты упорядоченные по категории"""
    cat = Category.objects.get(category_name=category)
    products = Product.objects.filter(category=cat)
    return render(request, 'shop/base.html', context={
        'products': products,
    })


def cart_remove(request, product_id):
    """Удаление единицы товара"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('cart_detail')


def cart_delete(request, product_id):
    """Полное удаление товара"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart_detail')


class UserLogView(LoginView):
    """Вход"""
    form_class = UserLogForm
    template_name = 'shop/login_user.html'

    def get_success_url(self):
        return "/"


class UserRegView(CreateView):
    """Регистрация"""
    form_class = UserRegForm
    template_name = 'shop/sign_up.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


def signoutview(request):
    """Выход"""
    logout(request)
    return redirect('/')


def addtowish(request):
    """Добавление в Избранное"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            product = Product.objects.get(id=prod_id)
            if WishList.objects.filter(
                    product=prod_id, user=request.user.id):
                return JsonResponse(
                    {'status': 'Product Already added'})
            else:
                WishList.objects.create(user=request.user, product=product)
                return JsonResponse({'status': 'successfully added'})
        else:
            return JsonResponse({'status': 'Login to continue'})

    return redirect('/')


def deletewishlist(request):
    """Удаление из Избранного"""
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        product = Product.objects.get(id=prod_id)
        if product:
            WishList.objects.get(product=product).delete()
            return JsonResponse({'status': 'Successfully deleted'})
        else:
            return JsonResponse({'status': 'Product are not available'})
    else:
        return redirect('/')


def viewwishlist(request):
    user = User.objects.get(username=request.user.username)
    wish_products = WishList.objects.filter(user=user)
    return render(request, 'shop/wishlist.html', context={
        'wish_products': wish_products,
    })
