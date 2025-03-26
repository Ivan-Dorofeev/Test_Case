from django.contrib import admin
from .models import Poll, Question, PollLogic, User, Blacklist

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(PollLogic)
admin.site.register(User)
admin.site.register(Blacklist)