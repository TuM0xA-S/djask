from django.shortcuts import render, get_object_or_404
from .models import Question
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

PAGE_SIZE = 5


def question_detail(request, pk):
    qn = get_object_or_404(Question, pk=pk)
    return render(request, 'ask/question_detail.html', {'question': qn})


def question_list(request):
    all_questions = Question.objects.all()
    paginator = Paginator(all_questions, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        question_list = paginator.page(page)
    except PageNotAnInteger:
        question_list = paginator.page(1)
    except EmptyPage:
        question_list = paginator.page(paginator.num_pages)

    return render(request, 'ask/question_list.html', {
        'question_list': question_list,
    })
