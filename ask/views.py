from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, QueryDict
from .models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm, TagSearchForm
from django.urls import reverse
from django.db.models import Count

PAGE_SIZE = 5


def question_detail(request, pk):
    qn = get_object_or_404(Question, pk=pk)
    return render(request, 'ask/question_detail.html', {'question': qn})


def question_list(request):
    questions = Question.objects.all()
    form = TagSearchForm(request.GET)
    tag_search = False
    tags = None
    if form.is_valid():
        tag_search = True
        tags = form.cleaned_data['tags']
        questions = questions.filter(tags__name__in=tags).annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-updated')

    paginator = Paginator(questions, PAGE_SIZE)
    qd = request.GET.copy()
    if 'page' in qd:
        del qd['page']
    qs = qd.urlencode()
    page = request.GET.get('page')
    try:
        question_list = paginator.page(page)
    except PageNotAnInteger:
        question_list = paginator.page(1)
    except EmptyPage:
        question_list = paginator.page(paginator.num_pages)

    return render(
        request, 'ask/question_list.html', {
            'question_list': question_list,
            'tag_search': tag_search,
            'tags': tags,
            'query': qs
        })


def tag_search(request):
    if request.method == 'POST':
        form = TagSearchForm(request.POST)
        if form.is_valid():
            qd = QueryDict(mutable=True)
            qd['tags'] = request.POST['tags']
            return HttpResponseRedirect(
                f"{reverse('ask:question_list')}?{qd.urlencode()}")
    else:
        form = TagSearchForm()

    return render(request, 'ask/tag_search.html', {'form': form})


@login_required
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()
            question_form.save_m2m()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        question_form = QuestionForm()

    return render(request, 'ask/create_question.html', {'form': question_form})


@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        question_form = QuestionForm(instance=question, data=request.POST)
        if question_form.is_valid():
            question_form.save()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        question_form = QuestionForm(instance=question)

    return render(request, 'ask/edit_question.html', {'form': question_form})


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden()

    question.delete()

    return HttpResponseRedirect(reverse("ask:delete_question_done"))


@login_required
def delete_question_done(request):
    return render(request, 'ask/delete_question_done.html')


@login_required
def confirm_delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden()
    return render(request, 'ask/confirm_delete_question.html',
                  {'question': question})


@login_required
def create_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return HttpResponseRedirect(answer.get_absolute_url())
    else:
        answer_form = AnswerForm()

    return render(request, 'ask/create_answer.html', {'form': answer_form})


@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        answer_form = AnswerForm(instance=answer, data=request.POST)
        if answer_form.is_valid():
            answer_form.save()
            return HttpResponseRedirect(answer.get_absolute_url())
    else:
        answer_form = AnswerForm(instance=answer)

    return render(request, 'ask/edit_answer.html', {'form': answer_form})


@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.author != request.user:
        return HttpResponseForbidden()

    answer.delete()

    return HttpResponseRedirect(
        reverse("ask:delete_answer_done", args=[answer.question.pk]))


@login_required
def delete_answer_done(request, pk):
    return render(request, 'ask/delete_answer_done.html', {'pk': pk})


@login_required
def confirm_delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.author != request.user:
        return HttpResponseForbidden()
    return render(request, 'ask/confirm_delete_answer.html',
                  {'answer': answer})
