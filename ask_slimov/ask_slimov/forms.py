# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth.hashers import make_password
from ask_slimov.models import Profile

import urllib
from django.core.files import File

#
# login form
#
class LoginForm(forms.Form):
    login = forms.CharField(
            widget=forms.TextInput(
                attrs={ 'class': 'form-control', 'placeholder': 'me', }
                ),
            max_length=30,
            label="Логин"
            )
    password = forms.CharField(
            widget=forms.PasswordInput(
                attrs={ 'class': 'form-control', 'placeholder': '*******', }
                ),
            label="Пароль",
            required=True
            )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError(
                        u'Данный пользователь не активен'
                        )
        else:
            raise forms.ValidationError(
                    u'Указан неверный логин или пароль'
                    )

#
# signup form
#
class SignupForm(forms.Form):
    login = forms.CharField(
            widget=forms.TextInput(
                attrs={ 'class': 'form-control', 'placeholder': 'me', }
                ),
            max_length=30,
            label="Логин"
            )
    first_name = forms.CharField(
            widget=forms.TextInput(
                attrs={ 'class': 'form-control', 'placeholder': 'Иван', }
                ),
            max_length=30,
            label="Имя"
            )
    last_name = forms.CharField(
            widget=forms.TextInput(
                attrs={ 'class': 'form-control', 'placeholder': 'Иванов', }
                ),
            max_length=30,
            label="Фамилия"
            )
    email = forms.EmailField(
            widget=forms.TextInput(
                attrs={ 'class': 'form-control', 'placeholder': 'me@gmail.com', }
                ),
            required = False,
            max_length=254,
            label="E-mail"
            )
    password1 = forms.CharField(
            widget=forms.PasswordInput(
                attrs={ 'class': 'form-control', 'placeholder': '*****' }
                ),
            min_length=6,
            label="Пароль")
    password2 = forms.CharField(
            widget=forms.PasswordInput(
                attrs={ 'class': 'form-control', 'placeholder': '*****' }
                ),
            min_length=6,
            label="Повторите пароль")
    info = forms.CharField(
            widget=forms.TextInput(
                attrs={ 'class': 'form-control', 'placeholder': 'Молод и горяч', }
                ),
            required=False,
            label="Пара слов о себе"
            )
    avatar = forms.FileField(
            widget=forms.ClearableFileInput(
                attrs={ 'class': 'ask-signup-avatar-input', }
                ),
            required=False,
            label="Аватар")

    def clean_login(self):
        login = self.cleaned_data.get('login', '')

        try:
            u = User.objects.get(username=login)
            raise forms.ValidationError(u'Такой пользователь уже существует')
        except User.DoesNotExist:
            return login

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1', '')
        pass2 = self.cleaned_data.get('password2', '')

        if pass1 != pass2:
            raise forms.ValidationError(u'Пароли не совпадают')

    def save(self):
        data = self.cleaned_data
        password = data.get('password1')
        u = User()

        u.username = data.get('login')
        u.password = make_password(password)
        u.email = data.get('email')
        u.first_name = data.get('first_name')
        u.last_name = data.get('last_name')
        u.is_active = True
        u.is_superuser = False
        u.save()

        up = Profile()
        up.user = u
        up.info = data.get('info')

        if data.get('avatar') is None:
            image_url = 'http://api.adorable.io/avatars/100/%s.png' % u.username
            content = urllib.urlretrieve(image_url)
            up.avatar.save('%s.png' % u.username, File(open(content[0])), save=True)
        else:
            avatar = data.get('avatar')
            up.avatar.save('%s_%s' % (u.username, avatar.name), avatar, save=True)

        up.save()

        return authenticate(username=u.username, password=password)
