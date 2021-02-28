from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime


class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ask:question_detail', args=[self.id])

    def was_updated(self):
        return self.updated - self.published >= datetime.timedelta(seconds=5)


class Answer(models.Model):
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:200]

    def get_absolute_url(self):
        return reverse('ask:question_detail', args=[self.question.id
                                                    ]) + f'#ans{self.pk}'
