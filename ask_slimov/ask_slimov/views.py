# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from ask_slimov import helpers
from ask_slimov.models import Question, Answer, QuestionLike, Tag
from ask_slimov.forms import LoginForm, SignupForm
from ask_slimov.decorators import need_login

from django.contrib import auth

# new questions
def questions_new(request):
    questions = Question.objects.list_new()

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': 'Новые вопросы',
                'key': 'new',
            })

# hot questions
def questions_hot(request):
    questions = Question.objects.list_hot()

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': 'Лучшие вопросы',
                'key': 'hot',
            })

# questiong by tag
def questions_tag(request, tag):
    try:
        tag = Tag.objects.get_by_title(tag)
    except Tag.DoesNotExist:
        raise Http404()
    
    questions = Question.objects.list_tag(tag)

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': u'Тег ' + tag.title,
            })

# single question
def question(request, id):
    try:
        q = Question.objects.get_single(int(id))
    except Question.DoesNotExist:
        raise Http404

    return render(request, 'question.html', {
                'question': q,
            })

# logout
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)

# login form
def form_login(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
    else:
        form = LoginForm()

    return render(request, 'form_login.html', {
            'form': form,
        })

# register form
def form_signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()

    return render(request , 'form_signup.html', {
            'form': form,
        })

# new question form
@need_login
def form_question_new(request):
    return render(request , 'form_question_new.html', {})
