from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main.html'


class UserLoginView(LoginView):
    template_name = 'login.html'
    next_page = 'main'


class UserLogoutView(LogoutView):
    next_page = 'main'
