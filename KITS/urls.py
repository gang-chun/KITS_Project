# from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'KITS'
name: object
urlpatterns = [
    path('', views.home, name='home'),
    path('study_list/', views.study_list, name='study_list'),
    path('study/<int:pk>/study_detail/', views.study_detail, name='study_detail'),
    path('create_study/', views.create_study, name='create_study'),
    path('study/<int:pk>/edit', views.study_edit, name='study_edit'),
    path('study/<int:pk>/archive/', views.study_archive, name='study_archive'),
    path('kit_checkin/', views.kit_checkin, name='kit_checkin'),
    path('kit_list/', views.kit_list, name='kit_list'),
]
