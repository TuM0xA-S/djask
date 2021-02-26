from django.test import TestCase
from .models import Question
from django.contrib.auth.models import User
from .views import PAGE_SIZE
from django.urls import reverse


class QuestionDetailViewTests(TestCase):
    def test_question(self):
        u = User.objects.create(username="someguy", password="password")
        q = Question.objects.create(title="Question 222222.",
                                    body="123",
                                    author=u)
        q.answer_set.create(body="answer1", author=u)
        q.answer_set.create(body="answer2", author=u)
        response = self.client.get(q.get_absolute_url())
        self.assertContains(response, "someguy")
        self.assertContains(response, "Question 222222.")
        self.assertContains(response, "123")
        self.assertContains(response, "answer1")
        self.assertContains(response, "answer2")


class QuestionListViewTests(TestCase):
    def test_questions_on_one_page(self):
        u = User.objects.create(username="someguy", password="password")
        for i in range(PAGE_SIZE):
            Question.objects.create(title=f"Question {i}.",
                                    body="123",
                                    author=u)
        response = self.client.get(reverse("ask:question_list"))
        self.assertEquals(len(response.context["question_list"]), PAGE_SIZE)
        for i in range(PAGE_SIZE):
            self.assertContains(response, f"Question {i}.")
