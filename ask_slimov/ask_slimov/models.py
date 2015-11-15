from django.db import models
from django.contrib.auth.models import User

import datetime

# user profile
class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatars')
    info = models.TextField()


# tag
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
    
    title = models.CharField(max_length=30)
    color = models.CharField(max_length=2, choices=COLORS, default=BLACK)


# question
class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.datetime.now)
    tags = models.ManyToManyField(Tag)


# question-like
class QuestionLike(models.Model):
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)


# answer
class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    correct = models.BooleanField(default=False)


# answer-like
class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)
