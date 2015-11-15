# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from ask_slimov.models import Question, Tag

from random import choice, randint
import os

class Command(BaseCommand):
    help = 'Creates fake tags'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                action='store',
                dest='number',
                default=3,
                help='Number of tags for a question'
        )

    def handle(self, *args, **options):
        tags = [
                'javascript', 'java', 'c#', 'php', 'android', 'jquery', 'python',
                'html', 'css', 'c++', 'ios', 'mysql', 'objective-c', 'sql', 'asp.net',
                'ruby-on-rails', 'iphone', 'angularjs', 'regexp'
                ]

        colors = Tag.COLORS

        for tag in tags:
            if len(Tag.objects.filter(title=tag)) == 0:
                t = Tag()

                t.title = tag
                t.color = choice(colors)[0]
                t.save()

        number = int(options['number'])

        tags = Tag.objects.all()

        for q in Question.objects.all():
            self.stdout.write('question [%d]' % q.id)
            if len(q.tags.all()) < number:
                for i in range(0, number - len(q.tags.all())):
                    t = choice(tags)

                    if t not in q.tags.all():
                        q.tags.add(t)
