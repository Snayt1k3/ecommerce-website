from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, TemplateView
from profile_user.models import SellerStatistics

from .forms import UserLogForm, UserRegForm, Reviews, ReviewSellerForm
from .models import Category, Product, Review, ReviewImages, Orders, OrdersItem, PersonalArea, PromoCode, \
    ReviewSeller


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
    template_name = 'shop/main_page.html'
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
    promo_db = ''

    if request.method == 'GET':
        cart_products = Cart.objects.filter(user=request.user.id)

        total = 0
        for item in cart_products:
            total += item.sub_total()

        if request.GET.get('promo_code'):
            # Манипуляции с Промо
            promo = request.GET.get('promo_code')
            try:
                promo_db = get_object_or_404(PromoCode, name=promo, user=request.user)
            except:
                promo_db = ''

            if promo_db:
                if total > promo_db.from_the_price:
                    if promo_db.is_percent:
                        total = total * (promo_db.amount_of_discount / 100)
                    else:
                        total -= promo_db.amount_of_discount

                request.session['promo'] = {'amount_of_discount': promo_db.amount_of_discount,
                                            'is_percent': promo_db.is_percent,
                                            'name': promo_db.name}

        return render(request, 'shop/payment/checkout.html', context={
            'cart_products': cart_products,
            'total': total,
            'promo_db': promo_db
        })

    if request.method == 'POST':
        total = 0
        cart_items = Cart.objects.filter(user=request.user)
        current_order = Orders.objects.create(user=request.user, status='В сборке у продавца')
        user_profile = PersonalArea.objects.get(user=request.user)

        for cart_item in cart_items:

            # Манипуляции с CartItem
            total += cart_item.sub_total()
            cart_item.product.stock -= 1
            user_profile.all_spent_money += cart_item.sub_total()

            # Манипуляции С продавцом
            if cart_item.product.seller:
                seller_profile = PersonalArea.objects.get(user=cart_item.product.seller)
                seller_profile.all_earned_money += cart_item.sub_total()
                seller_profile.save(update_fields=['all_earned_money'])

                stat = SellerStatistics.objects.get(product=cart_item.product)
                stat.bought += 1
                stat.save()

            # Создание Item и его присоединение к order
            item = OrdersItem.objects.create(product=cart_item.product, quantity=cart_item.quantity)
            current_order.order_items.add(item)

            # Сохранение Кол-во продукта на складе и удаление корзины пользователя
            cart_item.product.save()
            cart_item.delete()
            user_profile.save()

        # Промокод
        promo_db = request.session.get('promo')
        if promo_db:

            if promo_db['is_percent']:
                total = total * (int(promo_db['amount_of_discount']) / 100)

            else:
                total = total - int(promo_db['amount_of_discount'])

            PromoCode.objects.get(name=promo_db['name'], user=request.user).delete()
            del promo_db

        current_order.total = total
        current_order.save()
        PromoCode.objects.create(name='promo500', user=request.user, amount_of_discount=500, is_percent=False,
                                 from_the_price=1000)

        return redirect('checkout_success')


class SellerProductsView(ListView):
    template_name = 'shop/seller_products.html'
    context_object_name = 'seller_products'

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return Product.objects.filter(seller=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user = User.objects.get(username=self.kwargs['username'])
        context['more_info_user'] = PersonalArea.objects.get(user=user)
        return context


class CheckFailed(TemplateView):
    template_name = 'shop/payment/checkout_failed.html'


class CheckSuccess(TemplateView):
    template_name = 'shop/payment/checkout_success.html'


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
