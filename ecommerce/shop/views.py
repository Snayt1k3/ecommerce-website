from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.core.files.storage import FileSystemStorage
from .forms import UserLogForm, UserRegForm, Reviews
from .models import Category, Product, Cart, CartItem, Review, ReviewImages


# Create your views here.


class HomeView(ListView):
    """Домашняя Страница"""
    paginate_by = 16
    model = Product
    context_object_name = 'products'
    template_name = 'shop/base.html'


def detail_view(request, slug):
    context = {'success_form': False}
    # Получение Товара
    product = Product.objects.get(slug=slug)

    # Если пост, то записываем отзыв в модель
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['feedback']

        user = User.objects.get(username=request.user.username)

        rev = Review(rating=rating, text=review, username=user, pr_slug=product)
        rev.save()

        # Проверка на наличие Отправленных Файлов

        if request.FILES:
            files = request.FILES.getlist('files')
            for file in files:
                fs = FileSystemStorage()
                # сохраняем на файловой системе
                filename = fs.save(file.name, file)
                ex = ReviewImages(img=filename, pr_slug=product, review_id=rev)
                ex.save()

        context['success_form'] = True

    # Характеристики из модели в виде list(tuple(key, val))

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


def _cart_id(request):
    """Создание Корзины"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """Добавление в корзину"""
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1, )
        cart_item.save()

    return redirect("cart_detail")


def cart_detail(request, total=0, cart_items=None, counter=0):
    """Отображение Самой корзины"""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
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
