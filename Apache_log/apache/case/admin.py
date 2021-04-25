from django.contrib import admin
from .models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    """Выводим на панель администратора необходимые данные"""
    list_display = ['ip', 'date', 'http_method', 'url_request', 'code_response', 'size_response']
    list_filter = ['date', 'http_method']
    search_fields = ['code_response', 'ip']


admin.site.register(LogEntry, LogEntryAdmin)
