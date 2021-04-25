from django.contrib.admin.models import LogEntry
from django.views.generic import ListView


class MainView(ListView):
    template_name = 'main.html'

    def get_queryset(self):
        return LogEntry.objects.all()[:10]
