# ВНИМАНИЕ: !ТУТ ЛЮТЕЙШАЯ КОПИПАСТНАЯ ХУЙНЯ СДЕЛАННАЯ ЧЕРЕЗ ЖОПУ!

from django.test import TestCase
from .models import Question, Answer
from django.contrib.auth.models import User
from .views import PAGE_SIZE
from django.urls import reverse
from http import HTTPStatus


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


class QuestionCreateViewTests(TestCase):
    def test_create_question_auth(self):
        User.objects.create_user(username="testuser", password="password")
        self.assertTrue(
            self.client.login(username="testuser", password="password"))
        resp = self.client.post(reverse('ask:create_question'), {
            'title': 'title111111111111111',
            'body': 'body222222222222222222'
        },
                                follow=True)

        self.assertContains(resp, 'title111111111111111')
        self.assertContains(resp, 'body222222222222222222')

    def test_create_question_unauth(self):
        resp = self.client.post(reverse('ask:create_question'), {
            'title': 'title',
            'body': 'body'
        },
                                follow=True)
        self.assertEquals(resp.request['PATH_INFO'], reverse('login'))


class QuestionDeleteViewTests(TestCase):
    def test_delete_question_yours(self):
        u1 = User.objects.create_user(username='user1', password='1')
        User.objects.create_user(username='user2', password='2')
        q = Question.objects.create(title='1111', body='2222', author=u1)
        self.assertTrue(self.client.login(username='user1', password='1'))
        resp = self.client.get(reverse('ask:delete_question', args=[q.pk]))
        self.assertEquals(resp['location'],
                          reverse('ask:delete_question_done'))

    def test_delete_question_of_another_user(self):
        u1 = User.objects.create_user(username='user1', password='1')
        u2 = User.objects.create_user(username='user2', password='2')
        q = Question.objects.create(title='1111', body='2222', author=u1)
        self.assertTrue(self.client.login(username='user2', password='2'))
        resp = self.client.get(reverse('ask:delete_question', args=[q.pk]))

        self.assertEquals(resp.status_code, HTTPStatus.FORBIDDEN)


class AnswerCreateViewTests(TestCase):
    def test_create_answer_auth(self):
        u = User.objects.create_user(username="testuser", password="password")
        q = Question.objects.create(title='question1111',
                                    body='2222',
                                    author=u)
        self.assertTrue(
            self.client.login(username="testuser", password="password"))
        resp = self.client.post(reverse('ask:create_answer', args=[q.pk]),
                                {'body': 'body222222222222222222'},
                                follow=True)

        self.assertContains(resp, 'body222222222222222222')
        self.assertContains(resp, 'question1111')

    def test_create_answer_unauth(self):
        u = User.objects.create_user(username="testuser", password="password")
        q = Question.objects.create(title='question1111',
                                    body='2222',
                                    author=u)
        resp = self.client.post(reverse('ask:create_answer', args=[q.pk]),
                                {'body': 'body'},
                                follow=True)
        self.assertEquals(resp.request['PATH_INFO'], reverse('login'))


class AnswerDeleteViewTests(TestCase):
    def test_delete_answer_yours(self):
        u1 = User.objects.create_user(username='user1', password='1')
        q = Question.objects.create(title='4444', body='3333', author=u1)
        a = Answer.objects.create(body='1111', author=u1, question=q)
        self.assertTrue(self.client.login(username='user1', password='1'))
        resp = self.client.get(reverse('ask:delete_answer', args=[a.pk]))
        self.assertEquals(resp['location'],
                          reverse('ask:delete_answer_done', args=[q.pk]))

    def test_delete_answer_of_another_user(self):
        u1 = User.objects.create_user(username='user1', password='1')
        u2 = User.objects.create_user(username='user2', password='2')

        q = Question.objects.create(title='4444', body='3333', author=u1)
        a = Answer.objects.create(body='1111', author=u2, question=q)
        self.assertTrue(self.client.login(username='user1', password='1'))
        resp = self.client.get(reverse('ask:delete_answer', args=[a.pk]))

        self.assertEquals(resp.status_code, HTTPStatus.FORBIDDEN)


class RegisterViewTests(TestCase):
    def test_register(self):
        self.client.post(
            reverse('register'),
            dict(username="new_user",
                 password1="LOLlol1234",
                 password2="LOLlol1234",
                 email="lol@mail.ru"))
        User.objects.get(username="new_user")


class TagSearchViewTests(TestCase):
    def test_tag_searh(self):
        u1 = User.objects.create_user(username='user1', password='1')
        q1 = Question.objects.create(title='title1', body='body1', author=u1)
        q1.tags.add('1')
        q2 = Question.objects.create(title='title2', body='body2', author=u1)
        q2.tags.add('2')
        resp = self.client.post(reverse('ask:tag_search'), {'tags': '1'},
                                follow=True)
        self.assertQuerysetEqual(resp.context['question_list'],
                                 ['<Question: title1>'])
