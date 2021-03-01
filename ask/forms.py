from django import forms
from . import models
from taggit.forms import TagField


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ('title', 'body', 'tags')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ('body', )


class TagSearchForm(forms.Form):
    tags = TagField()
