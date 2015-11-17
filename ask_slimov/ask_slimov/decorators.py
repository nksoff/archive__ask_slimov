# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from ask_slimov import helpers


# login required with 'continue' arg
def need_login(func):
    return login_required(func, redirect_field_name='continue')


# login required [for ajax]
def need_login_ajax(func):
    def check(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        return helpers.HttpResponseAjaxError(
                code = "no_auth",
                message = u'Требуется авторизация',
                )
    return check
