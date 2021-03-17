from django.contrib import admin
from django.urls import path

from .views import PollsListView, PollDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("polls", PollsListView.as_view(), name='polls_list'),
    path("polls/<int:number_poll_id>", PollDetailView.as_view(), name='poll_detail'),
]
