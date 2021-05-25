from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import TemplateView

from Acits.rest_api_test.rest_api_test.forms import AuthForm


class MainPage(TemplateView):
    template_name = 'main.html'


class AuthPage(LoginView):
    template_name = 'login_page.html'
    next_page = 'main.html'
