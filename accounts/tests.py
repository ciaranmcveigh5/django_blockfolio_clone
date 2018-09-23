from django.urls import resolve, reverse
from django.test import TestCase
from .views import signup, login

# class SignUpTests(TestCase):
#     def test_signup_status_code(self):
#         url = reverse('signup')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)

#     def test_signup_url_resolves_signup_view(self):
#         view = resolve('/signup/')
#         self.assertEquals(view.func, signup)

class LogInTests(TestCase):
    def test_Login_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_login_url_resolves_signup_view(self):
        view = resolve('/accounts/login')
        self.assertEquals(view.func, login)