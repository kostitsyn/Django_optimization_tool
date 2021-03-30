from django.contrib.auth import forms
import hashlib
from random import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from authapp.models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',
                  'email', 'avatar', 'age')

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        if data > 100:
            raise forms.ValidationError('Ого, видимо кто-то выпил эликсир бессмертия!!!')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        i = 0
        while i <= 9:
            if str(i) in data:
                raise forms.ValidationError('Имя должно содержать только буквы!!!')
            i += 1
        return data

    def save(self, **kwargs):
        user = super(ShopUserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'avatar', 'age')

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def __str__(self):
        return self.fields['avatar']


    def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError('Вы слишком молоды!')
        if data > 100:
            raise forms.ValidationError('Ого, видимо кто-то выпил эликсир бессмертия!!!')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        i = 0
        while i <= 9:
            if str(i) in data:
                raise forms.ValidationError('Имя должно содержать только буквы!!!')
            i += 1
        return data


class ShopUserProfileEditForm(forms.ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'about_me', 'gender')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.help_text = ''




