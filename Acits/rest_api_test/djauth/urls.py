from django.contrib import admin
from django.urls import path, include
from .views import MainView, UserLoginView, UserLogoutView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', MainView.as_view(), name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('', include('rest_api_test.urls'))
]
