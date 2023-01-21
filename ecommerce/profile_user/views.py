from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect

from shop.models import PersonalArea, Orders


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

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        avatar = request.FILES.get('avatar')
        email = request.POST.get('email')

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
