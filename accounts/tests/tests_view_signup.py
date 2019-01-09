from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.contrib.auth import get_user_model


from accounts.forms import SignUpForm
from accounts.views import signup
from bbs.views import home


User = get_user_model()
# Create your tests here.


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse(signup)
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        url = reverse(signup)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse(signup)
        data = {
            'username': 'john',
            'email': 'john@163.com',
            'password1': 'abc123456',
            'password2': 'abc123456',
        }
        self.response = self.client.post(url,data)
        self.home_url = reverse(home)

    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authenication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)



