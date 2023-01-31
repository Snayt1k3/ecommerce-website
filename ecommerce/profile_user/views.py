from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import UpdateView
from shop.models import PersonalArea, Orders, Product, Category, PromoCode, ReviewSeller

from .forms import EmailChangeForm, BecomeSellerForm
from .models import SellerStatistics


# Create your views here.


def profile_user_view(request, username):
    context = {}
    if not request.user.is_authenticated or request.user.username != username:
        return redirect('/')

    if not PersonalArea.objects.filter(user=request.user):
        PersonalArea.objects.create(user=request.user)

    context['more_info_user'] = PersonalArea.objects.get(user=request.user)
    context['history_orders'] = Orders.objects.filter(user=request.user, status='Получен')
    context['current_orders'] = Orders.objects.exclude(status='Получен').filter(user=request.user).order_by('-id')
    context['promos'] = PromoCode.objects.filter(user=request.user)
    context['seller_reviews'] = ReviewSeller.objects.filter(seller=request.user)

    return render(request, 'profile_user/profile_user.html', context)


def email_sent_view(request):
    """Отправка mail с кодом из 6 цифр"""
    if request.method == 'POST':

        if request.user.is_authenticated:

            auth_key = ''.join([str(randint(0, 9)) for _ in range(6)])
            request.session['auth_key'] = auth_key

            send_mail(
                'Confirm email',
                f'''Код для Подтверждения Почты - {auth_key} 
                Никому не сообщайте его''',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email])
            return JsonResponse({'status': 'Письмо С кодом было Отправлено ', 'error': False})
        else:
            return JsonResponse({'status': 'Что-то пошло не так', 'error': True})
    else:
        return redirect('/')


def email_confirm_view(request):
    """Обработка Кода пользователя"""
    if request.method == 'POST':

        key1 = request.session.get('auth_key')
        key2 = request.POST.get('auth_key').strip()
        if key1 == key2:

            profile_user = PersonalArea.objects.get(user=request.user)
            profile_user.email_confirm = True
            profile_user.save()

            del request.session['auth_key']

            return JsonResponse({'status': 'Success'})

        else:

            return JsonResponse({'status': 'Wrong Key'})
    else:
        return redirect('/')


def become_seller(request):
    form = BecomeSellerForm(request.user)
    if request.method == 'POST':
        form = BecomeSellerForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('become_seller_success')

    return render(request, 'profile_user/become_seller.html', {'form': form})


def product_seller_view(request):
    if request.method == 'POST':
        # Проверка Продавец Или нет
        profile_user = PersonalArea.objects.get(user=request.user)

        if profile_user.is_seller:
            # Вытаскиваем Данные
            product_name = request.POST.get('product_name')
            product_price = request.POST.get('product_price')
            description = request.POST.get('description')
            characteristics = request.POST.get('characteristics')
            category = request.POST.get('category')
            stock = request.POST.get('stock')

            # Работа с файлом
            img = request.FILES.get('img')
            fs = FileSystemStorage()
            # сохраняем на файловой системе
            img = fs.save(img.name, img)

            category = Category.objects.get(category_name=category)

            # Parse characteristics
            characteristics = characteristics.split(',')
            characteristics = [i.split('-') for i in characteristics]
            characteristics = ','.join([x for i in characteristics for x in i])

            product = Product.objects.create(name=product_name, price=product_price, description=description,
                                             characteristics=characteristics, category=category, stock=stock,
                                             img=img,
                                             seller=request.user)
            SellerStatistics.objects.create(product=product, user=request.user)
            profile_user.your_products.add(product)
            profile_user.save()
            return redirect('seller_product_ok')
        else:
            return redirect('profile')

    else:
        return render(request, 'profile_user/expose_product.html', context={
            'more_info_user': PersonalArea.objects.get(user=request.user),
        })


def seller_view(request):
    user_profile = PersonalArea.objects.get(user=request.user)
    if user_profile.is_seller:
        # Общая статистика Продавца
        your_products = user_profile.your_products.all()

        # Цикл сбора
        add_cart = 0
        remove_cart = 0
        add_wish_list = 0
        remove_wish_list = 0
        bought = 0
        for product in your_products:
            stat = SellerStatistics.objects.get(product=product)

            # Обновление Данных Счетчиков
            add_cart += stat.add_cart
            remove_cart += stat.remove_cart
            add_wish_list += stat.add_wish_list
            remove_wish_list += stat.remove_wish_list
            bought += stat.bought

        stats = SellerStatistics.objects.filter(user=request.user)

        return render(request, 'profile_user/seller_stats.html', context={
            'your_products': your_products,
            'more_info_user': user_profile,
            'stats': stats,
            'add_cart': add_cart,
            'remove_cart': remove_cart,
            'add_wish_list': add_wish_list,
            'remove_wish_list': remove_wish_list,
            'bought': bought,
        })
    else:
        return redirect('/')


class OrderDetailView(DetailView):
    template_name = 'profile_user/order_detail.html'
    model = Orders
    context_object_name = 'order'


class ProfileUserUpdate(UpdateView):
    model = PersonalArea
    success_url = '/'
    fields = ['first_name', 'last_name', 'phone', 'address', 'avatar']
    template_name = 'profile_user/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['more_info_user'] = PersonalArea.objects.get(user=self.request.user)
        return context


class SellerProductUpdateView(UpdateView):
    success_url = '/'
    model = Product
    fields = ['name', 'price', 'description', 'characteristics', 'category', 'img', 'stock']
    template_name = 'profile_user/update_product_seller.html'


class SellerFeedbackView(ListView):
    template_name = 'profile_user/seller_feedbacks.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return ReviewSeller.objects.filter(seller=user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['username'])
        seller = PersonalArea.objects.get(user=user)
        context['more_info_user'] = seller

        # Пересчет Рейтинга Продавца
        reviews = ReviewSeller.objects.filter(seller=user)
        rating = 0.0
        for review in reviews:
            rating += float(review.rating)

        rating = round(rating / len(reviews), 1)
        seller.avg_rating = rating
        seller.save()

        return context


class BecomeSellerSuccess(TemplateView):
    template_name = 'profile_user/success_seller.html'


class ProductSellerSuccess(TemplateView):
    template_name = 'profile_user/success_seller_product.html'


def change_email(request):
    form = EmailChangeForm(request.user)
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            user = PersonalArea.objects.get(user=request.user)
            user.email_confirm = False
            user.save()
            return redirect('profile', username=request.user.username)

    return render(request, 'profile_user/change_email.html', {'form': form})
