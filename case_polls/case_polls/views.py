from django.views import generic

from .models import Polls


class PollsListView(generic.ListView):
    model = Polls
    template_name = 'polls_list.html'
    context_object_name = 'polls_list'


class PollDetailView(generic.DetailView):
    model = Polls
    template_name = 'poll_detail.html'
    context_object_name = 'poll_detail'
