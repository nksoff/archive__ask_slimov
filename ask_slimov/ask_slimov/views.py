# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from ask_slimov import helpers
from ask_slimov.models import Question, Answer, QuestionLike, Tag
from ask_slimov.forms import LoginForm, SignupForm, ProfileEditForm, AnswerForm
from ask_slimov.decorators import need_login

from django.contrib import auth
from django.forms.models import model_to_dict

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

    if request.method == "POST":
        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            answer = answer_form.save(q, request.user)
            return HttpResponseRedirect('#answer_' + str(answer.id))
    else:
        answer_form = AnswerForm()

    return render(request, 'question.html', {
                'question': q,
                'answer_form': answer_form,
            })


# logout
@need_login
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

    return render(request, 'form_signup.html', {
            'form': form,
        })


# profile edit form
@need_login
def form_profile_edit(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('')
    else:
        u = model_to_dict(request.user)
        up = request.user.profile
        u['info'] = up.info
        form = ProfileEditForm(u)

    return render(request, 'form_profile_edit.html', {
            'form': form,
            'u': request.user,
            'username': request.user.username,
        })


# new question form
@need_login
def form_question_new(request):
    return render(request, 'form_question_new.html', {})
