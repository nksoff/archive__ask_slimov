# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.models import User
from ask_slimov.models import Question

from random import choice, randint
from faker import Factory
import os

class Command(BaseCommand):
    help = 'Creates fake questions'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                action='store',
                dest='number',
                default=10,
                help='Number of questions to add'
        )

    def handle(self, *args, **options):
        fake = Factory.create()

        number = int(options['number'])

        users = User.objects.all()[1:]

        starts = (
                u'Помогите! Ничего не получается!!!!',
                u'Я перепробовал всё, помогите.',
                u'Не нашел ни одного решения в интернете, спасите!!',
                u'Проблема следующая:',
                u'Уже третий день не сплю из-за возникшей проблемы',
                u'Я думаю, что кто-то из вас сталкивался с таким вопросом',
                u'Извините, я новичок в вопросах веба.',
                u'Привет всем! Сроки горят, нужна консультация.',
                u'Ненавижу Винду',
                u'Нашел косяк в исходниках MySQL 5.6'
                )

        for i in range(0, number):
            q = Question()

            q.title = fake.sentence(nb_words=randint(4, 6), variable_nb_words=True)
            q.text = u"%s %s %s" % (
                    choice(starts),
                    os.linesep,
                    fake.paragraph(nb_sentences=randint(4, 17), variable_nb_sentences=True),
                    )
            q.author = choice(users)
            q.save()
            self.stdout.write('added question [%d]' % (q.id))
