from django import forms
from django.utils.translation import gettext as _


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
