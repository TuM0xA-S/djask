from django import forms
from . import models


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ('title', 'body')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ('body', )
