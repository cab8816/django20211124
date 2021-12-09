import datetime

from django.contrib import admin
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.timezone import now


class QuestionQuerySet(models.QuerySet):
    def now_pub_date(self):
        return self.filter(pub_date =now())
class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model,using=self._db)
    def pubdate(self):
        return self.get_queryset().now_pub_date()

# 本例允许你从管理器 Person.people 直接调用 authors() 和 editors()。
class Question(models.Model):
    nowquestion = QuestionManager()

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?'
    )
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    qestion = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
