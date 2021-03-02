# from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'KITS'
name: object
urlpatterns = [
    path('', views.home, name='home'),
    path('study_list/', views.study_list, name='study_list'),
    path('create_study/', views.create_study, name='create_study'),
]
