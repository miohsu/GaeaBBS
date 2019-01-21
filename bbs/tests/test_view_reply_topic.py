from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from django.contrib.auth import get_user_model

from ..models import Board, Post, Topic
from ..forms import PostForm
from ..views import reply_topic

User = get_user_model()


class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='DjangoTest')
        self.username = 'john'
        self.password = 'root123456'
        user = User.objects.create_user(username=self.username, email='john@163.com', password=self.password)
        self.topic = Topic.objects.create(subject='TopicTest', board=self.board, starter=user)
        Post.objects.create(message='PostTest', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.id, 'topic_pk': self.topic.id})


class LoginRequiredReplyTests(ReplyTopicTestCase):
    def test_redirection(self):
        response = self.client.get(self.url)
        login_url = reverse('login')
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, passwoord=self.password)
        self.response = self.client.get(self.url, follow=True)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEqual(view.func, reply_topic)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        # self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, '<textarea', 0)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'helloTest'})

    def test_redirection(self):
        url = reverse('topic_posts', kwargs={'pk': self.board.id, 'topic_pk': self.topic.id})
        post_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, post_url)

    def test_reply_created(self):
        self.assertEqual(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def test_view_reply_invalid(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(self.url, data={})
        self.assertContains(response, 'is-invalid')


