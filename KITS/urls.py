from django.conf.urls import url
from . import views
from django.urls import path, re_path

app_name = 'KITS'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^home/$', views.home, name='home'),
    path('login/', views.login, name='login'),
]

