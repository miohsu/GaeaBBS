from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.contrib.auth import get_user_model
from django.test import Client

from .views import home
from .views import board_topics
from .views import new_topic
from .models import Board
from .models import Topic
from .models import Post
from .forms import NewTopicForm


User = get_user_model()

# Create your tests here.

class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='DjangoTest')
        url = reverse(home)
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_url_resolves_link_to_topics_page(self):
        board_topics_url = reverse(board_topics, kwargs={'pk': self.board.id})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django Test')

    def test_board_topics_view_success_status_code(self):
        url = reverse(board_topics, kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse(board_topics, kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse(board_topics, kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse(home)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class NewTopicsTests(TestCase):

    def setUp(self):
        Board.objects.create(name='Django',description='djangoTest')
        User.objects.create_user(username='john', email='john@163.com',password='123')


    def test_new_topic_view_success_status_code(self):
        url = reverse(new_topic, kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse(new_topic, kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse(new_topic, kwargs={'pk': 1})
        board_topics_url = reverse(board_topics, kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse(board_topics, kwargs={'pk': 1})
        homepage_url = reverse(home)
        new_topic_url = reverse(new_topic, kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_csrf(self):
        url = reverse(new_topic, kwargs={'pk': 1})
        response = self.client.get(url)
        data = {
            'subject': 'Test tile',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url,data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse(new_topic, kwargs={'pk':1})
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEqual(response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse(new_topic, kwargs={'pk':1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse(new_topic, kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

