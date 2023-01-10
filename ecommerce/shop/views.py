from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .forms import UserLogForm, UserRegForm, SentFeedBack
from .models import Category, Product, Cart, CartItem


# Create your views here.


class HomeView(ListView):
    paginate_by = 16
    model = Product
    context_object_name = 'products'
    template_name = 'shop/base.html'


class ProductView(DetailView):
    template_name = 'shop/detail_pr.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        good = kwargs['object'].characteristics
        goods_key = good.split(",")[::2]
        goods_val = good.split(",")[1::2]
        info = list(zip(goods_key, goods_val))
        context["info"] = info
        context['info_sm'] = info[:6]
        context['form'] = SentFeedBack()
        return context


def prod_by_category(request, category):
    cat = Category.objects.get(category_name=category)
    products = Product.objects.filter(category=cat)
    return render(request, 'shop/base.html', context={
        'products': products,
    })


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
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
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart_detail')


class UserLogView(LoginView):
    form_class = UserLogForm
    template_name = 'shop/login_user.html'

    def get_success_url(self):
        return "/"


class UserRegView(CreateView):
    form_class = UserRegForm
    template_name = 'shop/sign_up.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


def signoutview(request):
    logout(request)
    return redirect('/')