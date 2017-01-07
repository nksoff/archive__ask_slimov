# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

import datetime
from django.utils import timezone
from django.db.models import Count, Sum

from django.core.urlresolvers import reverse

from ask_slimov import helpers
from django.core.cache import cache

from random import choice


# user profile
class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()

    def __unicode__(self):
        return "[" + str(self.user.id) + "] " + self.user.username


#
# tags manager
#
class TagManager(models.Manager):
    # adds number of questions to each tag
    def with_question_count(self):
        return self.annotate(questions_count=Count('question'))

    # sorts tags using number of questions
    def order_by_question_count(self):
        return self.with_question_count().order_by('-questions_count')

    # searches using title
    def get_by_title(self, title):
        return self.get(title=title)

    # finds or creates
    def get_or_create(self, title):
        try:
            tag = self.get_by_title(title)
        except Tag.DoesNotExist:
            tag = self.create(title=title, color=choice(Tag.COLORS)[0])
        return tag

    # counts most popular tags
    def count_popular(self):
        return self.order_by_question_count().all()[:20]


#
# tag
#
class Tag(models.Model):
    GREEN = 'success'
    DBLUE = 'primary'
    BLACK = 'default'
    RED = 'danger'
    LBLUE = 'info'
    COLORS = (
        ('GR', GREEN),
        ('DB', DBLUE),
        ('B', BLACK),
        ('RE', RED),
        ('BL', LBLUE)
    )

    title = models.CharField(max_length=30,
                             verbose_name='Название')
    color = models.CharField(max_length=2,
                             choices=COLORS,
                             default=BLACK,
                             verbose_name='Цвет')

    objects = TagManager()

    def get_url(self):
        return reverse('tag', kwargs={'tag': self.title})

    def __unicode__(self):
        return "[" + str(self.id) + "] " + self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color',)
    search_fields = ('title',)

    def get_ordering(self, request):
        return ['title']

    def get_list_filter(self, request):
        return ['color']


#
# custom query set for questions
#
class QuestionQuerySet(models.QuerySet):
    # preloads tags
    def with_tags(self):
        return self.prefetch_related('tags')

    # preloads answers
    def with_answers(self):
        res = self.prefetch_related('answer_set')
        res = self.prefetch_related('answer_set__author')
        res = self.prefetch_related('answer_set__author__profile')
        return res

    # loads number of answers
    def with_answers_count(self):
        return self.annotate(answers=Count('answer__id', distinct=True))

    # loads author
    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    # order by popularity
    def order_by_popularity(self):
        return self.order_by('-likes')

    # filter by date
    def with_date_greater(self, date):
        return self.filter(date__gt=date)


#
# questions manager
#
class QuestionManager(models.Manager):
    # custom query set
    def get_queryset(self):
        res = QuestionQuerySet(self.model, using=self._db)
        return res.with_answers_count().with_author().with_tags()

    # list of new questions
    def list_new(self):
        return self.order_by('-date')

    # list of hot questions
    def list_hot(self):
        return self.order_by('-likes')

    # list of questions with tag
    def list_tag(self, tag):
        return self.filter(tags=tag)

    # single question
    def get_single(self, _id):
        res = self.get_queryset()
        return res.with_answers().get(pk=_id)

    # best questions
    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset() \
            .order_by_popularity() \
            .with_date_greater(week_ago)


#
# question
#
class Question(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User,
                               verbose_name='Автор')
    date = models.DateTimeField(default=timezone.now,
                                verbose_name='Дата')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Теги')
    likes = models.IntegerField(default=0,
                                verbose_name='Кол-во лайков')

    objects = QuestionManager()

    def get_url(self):
        return reverse('question', kwargs={'id': self.id})

    # current correct answer
    def get_correct_answer(self):
        try:
            ans = Answer.objects.get(question=self, correct=True)
        except Answer.DoesNotExist:
            ans = None
        return ans

    def __unicode__(self):
        text = self.title[:100]
        if len(self.title) > 100:
            text += '...'
        return "[" + str(self.id) + "] " + text

    class Meta:
        ordering = ['-date']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date',)
    search_fields = ('title', 'text',)
    readonly_fields = ('likes',)

    def get_ordering(self, request):
        return ['-date', 'title']

    def get_list_filter(self, request):
        return ['author', 'tags']


#
# question-likes manager
#
class QuestionLikeManager(models.Manager):
    # adds a condition: with question
    def has_question(self, question):
        return self.filter(question=question)

    # returns likes count (sum) for a question
    def sum_for_question(self, question):
        return self.has_question(question).aggregate(sum=Sum('value'))['sum']

    # adds a like or raises exception
    def add(self, author, question, value):
        if author.id == question.author.id:
            raise QuestionLike.OwnLike

        try:
            obj = self.get(
                author=author,
                question=question
            )
        except QuestionLike.DoesNotExist:
            obj = self.create(
                author=author,
                question=question,
                value=value
            )
            question.likes = self.sum_for_question(question)
            question.save()
        else:
            raise QuestionLike.AlreadyLike

    # add like if not exists
    def add_or_update(self, author, question, value):
        obj, new = self.update_or_create(
            author=author,
            question=question,
            defaults={'value': value}
        )

        question.likes = self.sum_for_question(question)
        question.save()
        return new


#
# question-like
#
class QuestionLike(models.Model):
    # like for own question is not allowed
    class OwnLike(Exception):
        def __init__(self):
            super(QuestionLike.OwnLike, self) \
                .__init__(u'Вы не можете голосовать за свой вопрос')

    # already liked
    class AlreadyLike(Exception):
        def __init__(self):
            super(QuestionLike.AlreadyLike, self) \
                .__init__(u'Вы уже голосовали за этот вопрос')

    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question,
                                 verbose_name='Вопрос')
    author = models.ForeignKey(User,
                               verbose_name='Автор')
    value = models.SmallIntegerField(default=1,
                                     verbose_name='Лайк?')

    objects = QuestionLikeManager()

    def __unicode__(self):
        s = "[" + str(self.id) + "] " + self.author.username + " "

        if int(self.value) > 0:
            s += "<3"
        else:
            s += "<!!3"

        s += " q" + str(self.question_id)
        return s

    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'val')
    readonly_fields = ('question', 'author')

    def val(self, obj):
        s = ''
        if int(obj.value) > 0:
            s += "<3"
        else:
            s += "<!!3"

        return s


#
# custom query set for answers
#
class AnswerQuerySet(models.QuerySet):
    # loads author
    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    # loads question
    def with_question(self):
        return self.select_related('question')

    # order by popularity
    def order_by_popularity(self):
        return self.order_by('-likes')

    # filter by date
    def with_date_greater(self, date):
        return self.filter(date__gt=date)


#
# answers manager
#
class AnswerManager(models.Manager):
    # custom query set
    def get_queryset(self):
        res = AnswerQuerySet(self.model, using=self._db)
        return res.with_author()

    # create
    def create(self, **kwargs):
        ans = super(AnswerManager, self).create(**kwargs)

        text = ans.text[:100]
        if len(ans.text) > 100:
            text += '...'

        helpers.comet_send_message(
            helpers.comet_channel_id_question(ans.question),
            u'Новый ответ (' + ans.author.last_name + ' ' +
            ans.author.first_name + '): ' + text
        )
        return ans

    # best answers
    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset() \
            .order_by_popularity() \
            .with_date_greater(week_ago)


#
# answer
#
class Answer(models.Model):
    text = models.TextField(verbose_name='Ответ')
    question = models.ForeignKey(Question,
                                 verbose_name='Вопрос')
    author = models.ForeignKey(User,
                               verbose_name='Автор')
    date = models.DateTimeField(default=timezone.now,
                                verbose_name='Дата')
    correct = models.BooleanField(default=False,
                                  verbose_name='Правильный')
    likes = models.IntegerField(default=0,
                                verbose_name='Кол-во лайков')

    objects = AnswerManager()

    # makes this answer correct
    def set_correct(self, user=None):
        q = self.question

        if user is not None and q.author.id != user.id:
            raise Exception(u'Вы не являетесь автором этого вопроса')

        current = q.get_correct_answer()

        if current is not None:
            current.set_incorrect()

        self.correct = True
        self.save()

    # makes this answer incorrect
    def set_incorrect(self):
        self.correct = False
        self.save()

    def __unicode__(self):
        text = self.text[:100]
        if len(self.text) > 100:
            text += '...'
        return "[" + str(self.id) + "] " + text

    class Meta:
        ordering = ['-correct', '-date', '-likes']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'author', 'date', 'correct')
    search_fields = ('text',)
    readonly_fields = ('likes',)

    def get_ordering(self, request):
        return ['-date']

    def get_list_filter(self, request):
        return ['author', 'correct']


#
# answer-likes manager
#
class AnswerLikeManager(models.Manager):
    # adds a condition: with answer
    def has_answer(self, answer):
        return self.filter(answer=answer)

    # returns likes count (sum) for an answer
    def sum_for_answer(self, answer):
        return self.has_answer(answer).aggregate(sum=Sum('value'))['sum']

    # adds a like or raises exception
    def add(self, author, answer, value):
        if author.id == answer.author.id:
            raise AnswerLike.OwnLike

        try:
            obj = self.get(
                author=author,
                answer=answer
            )
        except AnswerLike.DoesNotExist:
            obj = self.create(
                author=author,
                answer=answer,
                value=value
            )
            answer.likes = self.sum_for_answer(answer)
            answer.save()
        else:
            raise AnswerLike.AlreadyLike

    # adds a like if not exists
    def add_or_update(self, author, answer, value):
        obj, new = self.update_or_create(
            author=author,
            answer=answer,
            defaults={'value': value}
        )

        answer.likes = self.sum_for_answer(answer)
        answer.save()
        return new


#
# answer-like
#
class AnswerLike(models.Model):
    # like for own answer is not allowed
    class OwnLike(Exception):
        def __init__(self):
            super(AnswerLike.OwnLike, self) \
                .__init__(u'Вы не можете голосовать за свой ответ')

    # already liked
    class AlreadyLike(Exception):
        def __init__(self):
            super(AnswerLike.AlreadyLike, self) \
                .__init__(u'Вы уже голосовали за этот ответ')

    UP = 1
    DOWN = -1

    answer = models.ForeignKey(Answer,
                               verbose_name='Ответ')
    author = models.ForeignKey(User,
                               verbose_name='Автор')
    value = models.SmallIntegerField(default=1,
                                     verbose_name='Лайк?')

    objects = AnswerLikeManager()

    def __unicode__(self):
        s = "[" + str(self.id) + "] " + self.author.username + " "

        if int(self.value) > 0:
            s += "<3"
        else:
            s += "<!!3"

        s += " a" + str(self.answer_id)
        return s

    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('answer', 'author', 'val')
    readonly_fields = ('answer', 'author')

    def val(self, obj):
        s = ''
        if int(obj.value) > 0:
            s += "<3"
        else:
            s += "<!!3"

        return s


# caching
class ProjectCache:
    #
    # popular tags
    #
    POPULAR_TAGS = 'tags_popular'

    # get
    @classmethod
    def get_popular_tags(cls):
        return cache.get(ProjectCache.POPULAR_TAGS, [])

    # update
    @classmethod
    def update_popular_tags(cls):
        popular = Tag.objects.count_popular()
        cache.set(ProjectCache.POPULAR_TAGS, popular, 60 * 60 * 24)

    #
    # best users
    #
    BEST_USERS = 'users_best'

    # get
    @classmethod
    def get_best_users(cls):
        return cache.get(ProjectCache.BEST_USERS, [])

    # update
    @classmethod
    def update_best_users(cls):
        best_answers = Answer.objects.get_best()
        best_questions = Question.objects.get_best()

        users = {}
        for i in best_answers:
            users[i.author_id] = users.get(i.author_id, 0) + i.likes
        for i in best_questions:
            users[i.author_id] = users.get(i.author_id, 0) + i.likes

        users = sorted(users, key=users.get)
        users.reverse()

        users = User.objects.filter(pk__in=users[:20])

        cache.set(ProjectCache.BEST_USERS, users, 60 * 60 * 24)
