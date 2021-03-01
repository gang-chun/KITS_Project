# from django.conf.urls import url
from . import views
from django.urls import path, re_path

app_name = 'KITS'
name: object
urlpatterns = [
    path('', views.home, name='home'),
    path('study/', views.study, name='study'),
    path('create_study/', views.create_study, name = 'create_study'),
]
