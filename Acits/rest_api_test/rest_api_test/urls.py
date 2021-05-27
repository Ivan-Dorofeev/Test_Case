from django.contrib import admin
from django.urls import path, include

from rest_api_test.rest_api_test.views import MainPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('', include('djauth')),
]
