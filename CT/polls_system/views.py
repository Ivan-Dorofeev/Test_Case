from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Poll, Question, PollLogic, User, Blacklist
from .forms import PollForm, QuestionForm, PollLogicForm, UserForm, BlacklistForm

# Опросы
class PollListView(ListView):
    model = Poll
    template_name = 'polls/poll_list.html'

class PollDetailView(DetailView):
    model = Poll
    template_name = 'polls/poll_detail.html'

class PollCreateView(CreateView):
    model = Poll
    form_class = PollForm
    template_name = 'polls/poll_form.html'
    success_url = '/polls/'

class PollUpdateView(UpdateView):
    model = Poll
    form_class = PollForm
    template_name = 'polls/poll_form.html'
    success_url = '/polls/'

class PollDeleteView(DeleteView):
    model = Poll
    template_name = 'polls/poll_confirm_delete.html'
    success_url = '/polls/'

# Пользователи
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = '/users/'

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = '/users/'

# Чёрные списки
class BlacklistListView(ListView):
    model = Blacklist
    template_name = 'blacklists/blacklist_list.html'

class BlacklistCreateView(CreateView):
    model = Blacklist
    form_class = BlacklistForm
    template_name = 'blacklists/blacklist_form.html'
    success_url = '/blacklists/'

class BlacklistUpdateView(UpdateView):
    model = Blacklist
    form_class = BlacklistForm
    template_name = 'blacklists/blacklist_form.html'
    success_url = '/blacklists/'