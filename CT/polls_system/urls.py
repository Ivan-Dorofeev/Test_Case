from django.urls import path
from .views import (
    PollListView, PollDetailView, PollCreateView, PollUpdateView, PollDeleteView,
    UserListView, UserCreateView, UserUpdateView,
    BlacklistListView, BlacklistCreateView, BlacklistUpdateView
)

urlpatterns = [
    # Опросы
    path('polls/', PollListView.as_view(), name='poll-list'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/create/', PollCreateView.as_view(), name='poll-create'),
    path('polls/<int:pk>/update/', PollUpdateView.as_view(), name='poll-update'),
    path('polls/<int:pk>/delete/', PollDeleteView.as_view(), name='poll-delete'),

    # Пользователи
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),

    # Чёрные списки
    path('blacklists/', BlacklistListView.as_view(), name='blacklist-list'),
    path('blacklists/create/', BlacklistCreateView.as_view(), name='blacklist-create'),
    path('blacklists/<int:pk>/update/', BlacklistUpdateView.as_view(), name='blacklist-update'),
]