import re
from random import randint

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from shop.models import PersonalArea, Orders, Product, Category

from .models import SellerStatistics


# Create your views here.


def profile_user_view(request, username):
    context = {}
    if not request.user.is_authenticated or request.user.username != username:
        return redirect('/')

    if not PersonalArea.objects.filter(user=request.user):
        PersonalArea.objects.create(user=request.user)

    more_info_user = PersonalArea.objects.get(user=request.user)
    history_orders = Orders.objects.filter(user=request.user, status='Получен')
    current_orders = Orders.objects.exclude(status='Получен').filter(user=request.user).order_by('-id')

    context['more_info_user'] = more_info_user
    context['history_orders'] = history_orders
    context['current_orders'] = current_orders

    return render(request, 'profile_user/profile_user.html', context)


def profile_user_edit_view(request, username):
    if not request.user.is_authenticated or request.user.username != username:
        return redirect('/')

    if request.method == 'POST':

        # Вытаскиваем Данные
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        avatar = request.FILES.get('avatar')
        email = request.POST.get('email')

        # Получение пользователя и его профиля
        user = User.objects.get(username=username)
        user_profile = PersonalArea.objects.get(user=user)

        # Проверки, что надо сохранить
        if email:
            user.email = email
            user_profile.email_confirm = False

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

        return render(request, 'profile_user/profile_edit.html', context={
            'more_info_user': user_profile
        })


def email_sent_view(request):
    """Отправка mail с кодом из 6 цифр"""
    if request.method == 'POST':

        if request.user.is_authenticated:

            auth_key = ''.join([str(randint(0, 9)) for _ in range(6)])
            request.session['auth_key'] = auth_key

            send_mail(
                'Confirm email',
                f'Код для Подтверждения Почты - {auth_key} Никому не сообщайте его',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email])

            return JsonResponse({'status': 'Email has been send', 'error': False})

        else:
            return JsonResponse({'status': 'Something went wrong', 'error': True})
    else:
        return redirect('/')


def email_confirm_view(request):
    """Обработка Кода пользователя"""
    if request.method == 'POST':

        key1 = request.session.get('auth_key')
        key2 = request.POST.get('auth_key')
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
    if request.method == 'POST':
        # Получение пользователя и его доп профиля
        user = User.objects.get(username=request.user.username)
        user_profile = PersonalArea.objects.get(user=user)

        # Получение данных с формы
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        # Валидация
        if not user_profile.email_confirm:
            messages.error(request, 'Подтвердите Почту чтобы продолжить')
        else:
            if not re.fullmatch(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', phone):
                messages.error(request, 'Телефон Введен Некорректно')
            else:
                if not user.check_password(password):
                    messages.error(request, "Неверный Пароль")
                else:
                    if not user.email == email:
                        user_profile.email_confirm = False

                    # Запись данных
                    user_profile.is_seller = True
                    user_profile.phone = phone
                    user.email = email
                    user_profile.save()
                    user.save()
                    return redirect('become_seller_success')

        return render(request, 'profile_user/become_seller.html', context={'phone': phone})
    else:
        return render(request, 'profile_user/become_seller.html')


class BecomeSellerSuccess(TemplateView):
    template_name = 'profile_user/success_seller.html'


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
            characteristics = ','.join([x for i in characteristics for x in i ])

            product = Product.objects.create(name=product_name, price=product_price, description=description,
                                             characteristics=characteristics, category=category, stock=stock,
                                             img='https://bipbap.ru/wp-content/uploads/2017/04/0_7c779_5df17311_orig.jpg',
                                             seller=request.user)
            SellerStatistics.objects.create(product=product, user=request.user)
            profile_user.your_products.add(product)
            profile_user.save()
            return redirect('seller_product_ok')
        else:
            return redirect('profile')

    else:
        more_info_user = PersonalArea.objects.get(user=request.user)

        return render(request, 'profile_user/products_seller.html', context={
            'more_info_user': more_info_user,
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

        return render(request, 'profile_user/seller.html', context={
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


class SellerProductUpdateView(UpdateView):
    success_url = '/'
    model = Product
    fields = ['name', 'price', 'description', 'characteristics', 'category', 'img', 'stock']
    template_name = 'profile_user/update_product_seller.html'


class ProductSellerSuccess(TemplateView):
    template_name = 'profile_user/success_seller_product.html'
