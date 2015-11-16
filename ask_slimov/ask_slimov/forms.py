# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms

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
