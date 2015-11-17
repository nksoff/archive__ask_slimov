# -*- coding: utf-8 -*-
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST

from ask_slimov import helpers
from ask_slimov.models import Question, Answer, QuestionLike, AnswerLike, Tag
from ask_slimov.forms import LoginForm, SignupForm, ProfileEditForm, AnswerForm, QuestionForm
from ask_slimov.decorators import need_login, need_login_ajax


# new questions
def questions_new(request):
    questions = Question.objects.list_new()

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': 'Новые вопросы', 'key': 'new',
            })


# hot questions
def questions_hot(request):
    questions = Question.objects.list_hot()

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': 'Лучшие вопросы', 'key': 'hot',
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
        form = ProfileEditForm(request.POST, request.FILES)
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
        })


# new question form
@need_login
def form_question_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(request.user)
            return HttpResponseRedirect(reverse('question', kwargs={'id': q.id}))
    else:
        form = QuestionForm()

    return render(request, 'form_question_new.html', {
        'form': form,
        })


# ajax question like
@need_login_ajax
def ajax_question_like(request, id):
    try:
        q = Question.objects.get(pk=id)
        value = int(request.POST.get('value', QuestionLike.UP))
        if value != QuestionLike.UP and value != QuestionLike.DOWN:
            value = QuestionLike.UP
        QuestionLike.objects.add(author=request.user, question=q, value=value)
        q = Question.objects.get(pk=id)
        return helpers.HttpResponseAjax(likes=q.likes, question_id=q.id)
    except Question.DoesNotExist:
        return helpers.HttpResponseAjaxError(code=u'no_question', message=u'Такого вопроса нет')
    except QuestionLike.AlreadyLike as e1:
        return helpers.HttpResponseAjaxError(code=u'already_like', message=e1.message)
    except QuestionLike.OwnLike as e2:
        return helpers.HttpResponseAjaxError(code=u'own_like', message=e2.message)


# ajax answer like
@need_login_ajax
@require_POST
def ajax_answer_like(request, id):
    try:
        ans = Answer.objects.get(pk=id)
        value = int(request.POST.get('value', AnswerLike.UP))
        if value != AnswerLike.UP and value != AnswerLike.DOWN:
            value = AnswerLike.UP
        AnswerLike.objects.add(author=request.user, answer=ans, value=value)
        ans = Answer.objects.get(pk=id)
        return helpers.HttpResponseAjax(likes=ans.likes, answer_id=ans.id)
    except Answer.DoesNotExist:
        return helpers.HttpResponseAjaxError(code=u'no_answer', message=u'Такого ответа нет')
    except AnswerLike.AlreadyLike as e1:
        return helpers.HttpResponseAjaxError(code=u'already_like', message=e1.message)
    except AnswerLike.OwnLike as e2:
        return helpers.HttpResponseAjaxError(code=u'own_like', message=e2.message)


# ajax answer correct
@need_login_ajax
@require_POST
def ajax_answer_correct(request, id):
    try:
        ans = Answer.objects.get(pk=id)
        ans.set_correct(request.user)
        return helpers.HttpResponseAjax(answer_id=ans.id)
    except Answer.DoesNotExist:
        return helpers.HttpResponseAjaxError(code=u'no_answer', message=u'Такого ответа нет')
    except Exception as e:
        return helpers.HttpResponseAjaxError(code=u'error', message=e.message)
