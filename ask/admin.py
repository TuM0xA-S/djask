from django.contrib import admin
from .models import Question, Answer

admin.AdminSite.site_header = "Djask Administration"


class AnswerInline(admin.StackedInline):
    model = Answer
    raw_id_fields = ('author', )
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'updated')
    list_filter = ('author', 'published', 'updated')
    ordering = ('-updated', )
    search_field = ('title', 'body')
    inlines = (AnswerInline, )
    raw_id_fields = ('author', )
    fields = (
        'author',
        'title',
        'body',
    )
