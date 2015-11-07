# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from ask_slimov import helpers

# new questions
def questions_new(request):
    from random import choice, randint
    tags = ['mysql', 'technopark', 'mail.ru', 'php', 'perl', 'ruby on rails', 'paraboloid', 'binary tree', 'css', 'json', 'cpp', 'binary-tree', 'bootstrap css', 'social network', 'c++11', ]
    colors = ['success', 'primary', 'default', 'danger', 'info']
    tags = [{ 'tag': tag, 'color': choice(colors), } for tag in tags]

    questions = [
        {
            'id': i,
            'title': 'Question ##' + str(i),
            'text': 'Hey, guys! Sorry for my English. The question: At what value of variable n the following code will cause memory leaks?',
            'votes': i + randint(1, i*10),
            'answers': i + randint(0, 5),
            'tags': [choice(tags) for j in range(0, i % 3 + 1)],
        } for i in range(1, 45)
    ]

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': 'Новые вопросы',
                'key': 'new',
            })

# hot questions
def questions_hot(request):
    from random import choice, randint
    tags = ['mysql', 'technopark', 'mail.ru', 'php', 'perl', 'ruby on rails', 'paraboloid', 'binary tree', 'css', 'json', 'cpp', 'binary-tree', 'bootstrap css', 'social network', 'c++11', ]
    colors = ['success', 'primary', 'default', 'danger', 'info']
    tags = [{ 'tag': tag, 'color': choice(colors), } for tag in tags]

    questions = [
        {
            'id': i,
            'title': 'Hot Question ##' + str(i),
            'text': 'Hey, guys! Sorry for my English. The question: At what value of variable n the following code will cause memory leaks?',
            'votes': i + randint(1, i*10),
            'answers': i + randint(0, 5),
            'tags': [choice(tags) for j in range(0, i % 3 + 1)],
        } for i in range(1, 45)
    ]

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': 'Лучшие вопросы',
                'key': 'hot',
            })

# questiong by tag
def questions_tag(request, tag):
    from random import randint

    questions = [
        {
            'id': i,
            'title': 'Tag Question ##' + str(i),
            'text': 'Hey, guys! Sorry for my English. The question: At what value of variable n the following code will cause memory leaks?',
            'votes': i + randint(1, i*10),
            'answers': i + randint(0, 5),
            'tags': [{'tag': tag, 'color': 'info',}],
        } for i in range(1, 45)
    ]

    pagination = helpers.paginate(questions, request)
    return render(request, 'questions_list.html',
            {
                'questions': pagination,
                'title': 'Тег ' + str(tag),
            })

# single question
def question(request, id):
    id = int(id)
    from random import choice, randint
    tags = ['mysql', 'technopark', 'mail.ru', 'php', 'perl', 'ruby on rails', 'paraboloid', 'binary tree', 'css', 'json', 'cpp', 'binary-tree', 'bootstrap css', 'social network', 'c++11', ]
    colors = ['success', 'primary', 'default', 'danger', 'info']
    tags = [{ 'tag': tag, 'color': choice(colors), } for tag in tags]

    answers = [
            {'text': 'I don\'t really know, sorry!', 'votes': id + randint(-5, id), 'correct': i == 0} for i in range(0, 5)
            ]

    q = {
            'id': id,
            'title': 'Question ##' + str(id),
            'text': 'Hey, guys! Sorry for my English. The question: At what value of variable n the following code will cause memory leaks?',
            'votes': id + randint(1, id*10),
            'tags': [choice(tags) for i in range(0, 3)],
            'answers': answers,
        }
    return render(request, 'question.html', q)

# login form
def form_login(request):
    return render(request , 'form_login.html', {})

# register form
def form_signup(request):
    return render(request , 'form_signup.html', {})

# new question form
def form_question_new(request):
    return render(request , 'form_question_new.html', {})

def info(request):
    to_show = [
        ['GET - параметры', request.GET],
        ['POST - параметры', request.POST]
    ]

    output = ['<html>', '<h1>%s</h1>' % 'Привет, мир!']

    for params in to_show:
        output.append('<h3>%s (%d)</h3>'
                % (params[0], len(params[1])))
        output.append('<pre>')

        output.extend(
            [
                "%s ==> '%s' \n"
                    % (k, v) for k,v in params[1].items()
            ]
        )

        output.append('</pre>')

    output.append('</html>')

    output.append('</html>')
    return HttpResponse(output)
