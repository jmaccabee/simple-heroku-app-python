import datetime

from django.db import models
from django.utils import timezone

from base.models import BaseAbstractModel


class Question(BaseAbstractModel):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """
        Set string methods for your models - they're used throughout the Django admin.
        """
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(BaseAbstractModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Set string methods for your models - they're used throughout the Django admin.
        """
        return self.choice_text
