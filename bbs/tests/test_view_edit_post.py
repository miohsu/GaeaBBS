from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Board, Post, Topic
from ..views import PostUpdateView

User = get_user_model()


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='DjangoTest')
        self.username = 'john'
        self.email = 'john@163.com'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        self.topic = Topic.objects.create(subject='Hello', board=self.board, starter=user)
        self.post = Post.objects.create(message='PostTest', topic=self.topic, created_by=user)
        self.url = reverse('edit_post',
                           kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk, 'post_pk': self.post.pk})


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        email = 'jane@163.com'
        password = '321'
        user = User.objects.create_user(username=username, email=email, password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 404)
