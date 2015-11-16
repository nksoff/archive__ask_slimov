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
    username = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'me', }),
            max_length=30, label="Логин"
            )
    first_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Иван', }),
            max_length=30, label="Имя"
            )
    last_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Иванов', }),
            max_length=30, label="Фамилия"
            )
    email = forms.EmailField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'me@gmail.com', }),
            required = False, max_length=254, label="E-mail"
            )
    password1 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': '*****' }),
            min_length=6, label="Пароль"
            )
    password2 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': '*****' }),
            min_length=6, label="Повторите пароль"
            )
    info = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Молод и горяч', }),
            required=False, label="Пара слов о себе"
            )
    avatar = forms.FileField(
            widget=forms.ClearableFileInput( attrs={ 'class': 'ask-signup-avatar-input', }),
            required=False, label="Аватар"
            )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError(u'Такой пользователь уже существует')
        except User.DoesNotExist:
            return username

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1', '')
        pass2 = self.cleaned_data.get('password2', '')

        if pass1 != pass2:
            raise forms.ValidationError(u'Пароли не совпадают')

    def save(self):
        data = self.cleaned_data
        password = data.get('password1')
        u = User()

        u.username = data.get('username')
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

#
# profile edit form
#
class ProfileEditForm(forms.Form):
    first_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Иван', }),
            max_length=30, label="Имя"
            )
    last_name = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Иванов', }),
            max_length=30, label="Фамилия"
            )
    email = forms.EmailField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'me@gmail.com', }),
            required = False, max_length=254, label="E-mail"
            )
    password1 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': '*****' }),
            min_length=6, label="Пароль", required=False
            )
    password2 = forms.CharField(
            widget=forms.PasswordInput( attrs={ 'class': 'form-control', 'placeholder': '*****' }),
            min_length=6, label="Повторите пароль", required=False
            )
    info = forms.CharField(
            widget=forms.TextInput( attrs={ 'class': 'form-control', 'placeholder': 'Молод и горяч', }),
            required=False, label="Пара слов о себе"
            )
    avatar = forms.FileField(
            widget=forms.ClearableFileInput( attrs={ 'class': 'ask-signup-avatar-input', }),
            required=False, label="Аватар"
            )

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1', '')
        pass2 = self.cleaned_data.get('password2', '')

        if pass1 != pass2:
            raise forms.ValidationError(u'Пароли не совпадают')

    def save(self, user):
        data = self.cleaned_data
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')

        pass1 = self.cleaned_data.get('password1', '')
        if pass1 != '':
            user.set_password(pass1)

        user.save()

        up = user.profile
        up.info = data.get('info')

        if data.get('avatar') is not None:
            avatar = data.get('avatar')
            up.avatar.save('%s_%s' % (user.username, avatar.name), avatar, save=True)

        up.save()

        return self

class AnswerForm(forms.Form):
    text = forms.CharField(
            widget=forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'placeholder': u'Введите ваш ответ', }
                ),
            required=True
            )

    def save(self, question, author):
        data = self.cleaned_data
        return question.answer_set.create(text=data.get('text'), author=author)
