from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm

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


@login_required
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        question_form = QuestionForm()

    return render(request, 'ask/create_question.html',
                  {'question_form': question_form})
