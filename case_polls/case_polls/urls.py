from django.urls import path

from .views import PollsListView, PollDetailView


urlpatterns = [
    path("polls", PollsListView.as_view(), name='polls_list'),
    path("polls/<int:number_poll_id>", PollDetailView.as_view(), name='poll_detail'),
]
