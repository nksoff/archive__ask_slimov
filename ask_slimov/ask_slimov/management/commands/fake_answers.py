# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from ask_slimov.models import Question, Answer

from random import choice, randint
from faker import Factory


class Command(BaseCommand):
    help = 'Creates fake answers'

    def add_arguments(self, parser):
        parser.add_argument('--min-number',
                            action='store',
                            dest='min_number',
                            default=5,
                            help='Min number of answers for a question'
                            )
        parser.add_argument('--max-number',
                            action='store',
                            dest='max_number',
                            default=15,
                            help='Max number of answers for a question'
                            )

    def handle(self, *args, **options):
        fake = Factory.create()

        min_number = int(options['min_number'])
        max_number = int(options['max_number'])

        users = User.objects.all()[1:]
        questions = Question.objects.all()

        for q in questions:
            for i in range(0, randint(min_number, max_number)):
                ans = Answer()

                ans.text = fake.paragraph(nb_sentences=randint(2, 10),
                                          variable_nb_sentences=True)
                ans.author = choice(users)
                ans.question = q
                ans.save()
                self.stdout.write('[%d] ans[%d]' % (q.id, ans.id))
