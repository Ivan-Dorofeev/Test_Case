from django.db import models


class LogEntry(models.Model):
    """Создаём модель данных, которые нам нужны"""
    ip = models.CharField(max_length=50)
    date = models.CharField(max_length=50)
    http_method = models.CharField(max_length=1500)
    url_request = models.CharField(max_length=1000)
    code_response = models.CharField(max_length=3)
    size_response = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.ip, self.date
