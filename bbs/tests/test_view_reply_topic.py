from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Board, Post, Topic
from ..views import reply_topic

User = get_user_model()


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='DjangoTest')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, password=self.password, email='john@163.com')
        self.topic = Topic.objects.create(subject='TopicTest', board=self.board, starter=user)
        Post.objects.create(message='PostTest', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.id, 'topic_pk': self.topic.id})


class LoginRequiredReplyTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()

    def test_redirection(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTests(ReplyTopicTestCase):
    def test_view_reply_response(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertContains(response, '<input', 1)
        self.assertContains(response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def test_view_status_code(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def test_view_reply_invalid(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data={})
        self.assertContains(response, 'is-invalid')
