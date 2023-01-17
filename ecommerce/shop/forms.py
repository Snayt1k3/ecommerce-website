from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserLogForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}), label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label='Пароль',)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ваш Email'}))


class UserRegForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}), label='Логин')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ваш Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label='Пароль',)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите Пароль'}),
                                label='Повторите Пароль')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class Reviews(forms.Form):
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Оставьте Отзыв', 'class': 'form-control', 'wrap': 'hard', }),
        required=False)
    files = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'right_menu form-control'}),
        required=False, label='Фото')
