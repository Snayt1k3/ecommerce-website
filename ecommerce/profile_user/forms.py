import re

from django import forms
from django.utils.translation import gettext as _
from shop.models import PersonalArea


class EmailChangeForm(forms.Form):
    error_messages = {
        'email_mismatch': _("Два поля адресов электронной почты не совпадают."),
        'not_changed': _("Адрес электронной почты совпадает с уже заданным."),
    }

    new_email1 = forms.EmailField(
        label=_("Новый Email"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=_("Подтвердите Email"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.cleaned_data.get('new_email1', None) != self.cleaned_data.get('new_email2', None):
            raise forms.ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch',
            )

        if self.user.email == self.cleaned_data.get('new_email1', None):
            raise forms.ValidationError(
                self.error_messages['not_changed'],
                code='not_changed',
            )

        return self.cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class BecomeSellerForm(forms.Form):
    error_messages = {
        'phone_invalid': _("Введите Телефон Корректно"),
        'password_invalid': _("Неверный Пароль"),
        'email_invalid': _('Неверный Email'),
        'email_not_confirm': _('Подтвердите Почту')
    }

    email = forms.EmailField(label='Ваш Электронный Адрес')
    phone = forms.CharField(max_length=30, label='Ваш Телефон')
    password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите Пароль')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(BecomeSellerForm, self).__init__(*args, **kwargs)

    def clean(self):
        phone = self.cleaned_data.get('phone', None)
        email = self.cleaned_data.get('email', None)
        password = self.cleaned_data.get('password', None)

        user_profile = PersonalArea.objects.get(user=self.user)

        if not user_profile.email_confirm:
            raise forms.ValidationError(
                self.error_messages['email_not_confirm'],
                code='email_not_confirm',
            )

        if not re.fullmatch(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', phone):
            raise forms.ValidationError(
                self.error_messages['phone_invalid'],
                code='phone_invalid',
            )

        if not self.user.check_password(password):
            raise forms.ValidationError(
                self.error_messages['password_invalid'],
                code='password_invalid',
            )

        if self.user.email != email:
            raise forms.ValidationError(
                self.error_messages['email_invalid'],
                code='email_invalid',
            )

        return self.cleaned_data

    def save(self, commit=True):
        user_profile = PersonalArea.objects.get(user=self.user)
        user_profile.phone = self.cleaned_data.get('phone')
        user_profile.is_seller = True
        user_profile.save()
        if commit:
            self.user.save()
        return self.user
