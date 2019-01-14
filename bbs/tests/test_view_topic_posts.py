from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse

from ..models import Board, Topic, Post
from ..views import topic_posts

User = get_user_model()


class TopicPostsTests(TestCase):
    def setUp(self):
        board = Board.objects.create(name='Django', description='DjangoTest')
        user = User.objects.create_user(username='john', email='john@163.com', password='123')
        topic = Topic.objects.create(subject='Hello world', board=board, starter=user)
        Post.objects.create(message='DjangePostTest', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.id, 'topic_pk': topic.id})
        self.response = self.client.get(url)

    def test_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEqual(view.func, topic_posts)
