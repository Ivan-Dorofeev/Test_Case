from django import forms
from .models import Poll, Question, PollLogic, User, Blacklist

# Форма для опроса
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'is_active']

# Форма для вопроса
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']

# Форма для логики опроса
class PollLogicForm(forms.ModelForm):
    class Meta:
        model = PollLogic
        fields = ['condition']

# Форма для пользователя
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone']

# Форма для чёрного списка
class BlacklistForm(forms.ModelForm):
    class Meta:
        model = Blacklist
        fields = ['user', 'reason']