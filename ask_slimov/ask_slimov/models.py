from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.db.models import Count, Sum

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
    
    title = models.CharField(max_length=30)
    color = models.CharField(max_length=2, choices=COLORS, default=BLACK)

    objects = TagManager()

    def __unicode__(self):
        return "[" + str(self.id) + "] " + self.title

#
# custom query set for questions
#
class QuestionQuerySet(models.QuerySet):
    # preloads tags
    def with_tags(self):
        return self.prefetch_related('tags')

    # loads number of answers
    def with_answers_count(self):
        return self.annotate(answers=Count('answer__id', distinct=True))

    # loads author
    def with_author(self):
        return self.select_related('author').select_related('author__profile')

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

#
# question
#
class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    objects = QuestionManager()

    def __unicode__(self):
        return "[" + str(self.id) + "] " + self.title

    class Meta:
        ordering = ['-date']


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

    # adds a like if not exists
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
    UP = 1
    DOWN = -1

    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)

    objects = QuestionLikeManager()

    def __unicode__(self):
        s = "[" + str(self.id) + "] " + self.author.username + " "

        if int(self.value) > 0:
            s += "<3"
        else:
            s += "<!!3"
        
        s += " q" + str(self.question_id)
        return s


#
# answers manager
#
class AnswerManager(models.Manager):
    # adds number of likes to each answer
    def with_likes(self):
        return self.annotate(likes=Sum('answerlike__value'))

    # sorts answers using rating (likes)
    def order_by_likes(self):
        return self.with_likes().order_by('-likes')

    # sorts answers using creation date
    def order_by_date(self):
        return self.order_by('-date')

    # add a condition: with author
    def has_author(self, author):
        return self.filter(author=author)


#
# answer
#
class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    objects = AnswerManager()

    def __unicode__(self):
        return "[" + str(self.id) + "] " + self.text

    class Meta:
        ordering = ['-date']


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
    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(User)
    value = models.SmallIntegerField(default=1)

    objects = AnswerLikeManager()

    def __unicode__(self):
        s = "[" + str(self.id) + "] " + self.author.username + " "

        if int(self.value) > 0:
            s += "<3"
        else:
            s += "<!!3"
        
        s += " a" + str(self.answer_id)
        return s
