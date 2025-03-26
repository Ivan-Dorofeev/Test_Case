from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель пользователя
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# Модель опроса
class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Модель вопроса
class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[('text', 'Text'), ('choice', 'Choice'), ('multiple', 'Multiple')])

    def __str__(self):
        return self.text

# Модель логики опроса
class PollLogic(models.Model):
    poll = models.OneToOneField(Poll, on_delete=models.CASCADE, related_name='logic')
    condition = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Logic for {self.poll.title}"

# Модель чёрного списка
class Blacklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blacklists')
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklist for {self.user.username}"