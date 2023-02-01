from decimal import Decimal

from cart.cart import Cart
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from profile_user.models import SellerStatistics

from .forms import UserLogForm, UserRegForm, Reviews, ReviewSellerForm
from .models import Category, Product, Review, Orders, PersonalArea, ReviewSeller, OrdersItem, PromoCode


# Create your views here.


class HomeView(ListView):
    """Домашняя Страница"""
    paginate_by = 16
    model = Product
    context_object_name = 'products'
    template_name = 'shop/main.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            object_list = Product.objects.filter(Q(name__icontains=query)).order_by('-stock')
        else:
            object_list = Product.objects.all().order_by('-stock')
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

            return redirect('one_pr', slug=slug)
        else:
            messages.error(request, 'У вас Уже есть отзыв на данный товар')

    # Получение Отзывов на товар
    context['reviews'] = Review.objects.filter(product=product)

    # Характеристики из модели
    good = product.characteristics
    goods_key = good.split(",")[::2]
    goods_val = good.split(",")[1::2]
    info = list(zip(goods_key, goods_val))
    context["info"] = info

    context['product'] = product
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

    if product.seller:
        context['seller_profile'] = PersonalArea.objects.get(user=product.seller)
        context['seller_products'] = Product.objects.filter(seller=context['seller_profile'].user)

    return render(request, 'shop/product_detail.html', context)


class ProductCategoryView(ListView):
    template_name = 'shop/main.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = Category.objects.get(category_name=self.kwargs['category'])
        return Product.objects.filter(category=category)


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
        PersonalArea.objects.create(user=user)
        login(self.request, user)
        return redirect(self.success_url)


def sign_out(request):
    """Выход"""
    logout(request)
    return redirect('/')


def checkout(request):
    """Оплата"""
    promo = request.session.get('promo')
    cart = Cart(request)
    total = cart.get_total_price()

    # Проверка промокода
    if promo:
        if promo['is_percent']:
            total = round((total * (int(promo['amount_of_discount']) / 100)), 2)
        else:
            total = total - int(promo['amount_of_discount'])

    # Косвенная Оплата
    if request.method == 'POST':
        # get data
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        zip_index = request.POST.get('zip_index')

        # create order
        order = Orders.objects.create(first_name=firstname, last_name=lastname, email=email, address=address,
                                      country=country, zip_index=zip_index, total=total)
        if request.user.is_authenticated:
            order.user = request.user

        if promo:
            PromoCode.objects.get(name=promo['name']).delete()

        for item in cart:
            product = Product.objects.get(name=item['product']['name'])

            # seller stats
            seller_stats = SellerStatistics.objects.get(product=product)
            seller_stats.bought += 1
            seller_stats.save()
            seller_profile = PersonalArea.objects.get(user=product.seller)
            seller_profile.all_earned_money += Decimal(product.price * item['quantity'])
            seller_profile.save()

            order_item = OrdersItem.objects.create(product=product, quantity=item['quantity'])

            # put order_item in order
            order.order_items.add(order_item)

            if request.user.is_authenticated:
                user_profile = PersonalArea.objects.get(user=request.user)
                user_profile.all_spent_money += Decimal(product.price * item['quantity'])
                user_profile.save()

        order.save()
        cart.clear()

        send_mail(
            f'Заказ {order.id}',
            f"""
            Спасибо за покупку, 
            Вы можете отследить свой заказ на сайте
            Ваш Заказ Под номером {order.id}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email])

        return render(request, 'shop/payment/checkout_success.html', {'order_id': order.id})

    return render(request, 'shop/payment/checkout.html', {'cart': cart, 'promo': promo, 'total': total})


class SellerProductsView(ListView):
    template_name = 'profile_user/seller_products.html'
    context_object_name = 'seller_products'

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return Product.objects.filter(seller=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user = User.objects.get(username=self.kwargs['username'])
        context['more_info_user'] = PersonalArea.objects.get(user=user)
        context['seller_stats'] = SellerStatistics.objects.filter(user=context['more_info_user'].user)
        return context


def feedback_seller(request, username):
    if request.method == 'POST':
        form = ReviewSellerForm(request.POST)

        seller = User.objects.get(username=username)
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        if rating and feedback:
            ReviewSeller.objects.create(feedback=feedback, seller=seller, rating=rating, username=request.user.username)
            return redirect('list_seller_products', username=username)
    else:
        form = ReviewSellerForm()
    return render(request, 'shop/feedback_seller.html', context={'form': form})


def get_order_for_anonymous(request):
    if request.method == 'POST':
        pk = request.POST.get('order_id')

        if Orders.objects.filter(pk=pk):
            return redirect('order_detail_pk', pk=pk)

    return render(request, 'shop/get_order.html')
