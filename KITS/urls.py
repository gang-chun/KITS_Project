# from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'KITS'
name: object
urlpatterns = [
    path('', views.home, name='home'),
    path('home2/', views.home2, name='home2'),
    path('study_list/', views.study_list, name='study_list'),
    path('study/<int:pk>/study_detail/', views.study_detail, name='study_detail'),
    path('study/<int:pk>/study_detail/kit_edit/', views.kit_edit, name='kit_edit_from_study'),

    path('create_study/', views.create_study, name='create_study'),
    path('study/<int:pk>/edit', views.study_edit, name='study_edit'),
    path('study/<int:pk>/archive/', views.study_archive, name='study_archive'),
    path('study/<int:pk>/create_req', views.create_req, name='create_req'),
    path('study/<int:pk>/study_detail/req_edit', views.req_edit, name='req_edit'),

    path('kit_list/kit_addtype/', views.kit_addkittype, name='kit_addkittype'),
    path('kit_list/kit_addlocation/', views.kit_addlocation, name='kit_addlocation'),

    path('kit_list/', views.kit_list, name='kit_list'),
    path('kit_list/<int:pk>/kit_edit/', views.kit_edit, name='kit_edit'),

    path('kit_list/<int:pk>/delete/', views.kit_delete, name='kit_delete'),
    path('kit_list/<int:pk>/kit_addkitinstance/', views.kit_addkitinstance, name='kit_addkitinstance'),

    path('report/', views.report, name='report'),
    path('report/report_expiredkits/', views.report_expiredkits, name='report_expiredkits'),
    path('report/report_expiredkits/studies', views.report_expiredkits_studies, name='report_expiredkits_studies'),

    path('study/<int:pk>/study_detail/kit_ordering', views.kit_ordering, name='kit_ordering'),
    path('study/<int:pk>/kit_ordering_add/', views.kit_ordering_add, name='kit_ordering_add'),
    #path('kit_list/kitinstance/<int:pk>/addkitinstance', views.kitinstance_add, name='kitinstance_add'),

    # path('kit_list/kitinstance/<int:pk>/addkitinstance', views.kitinstance_add, name='kitinstance_add'),





]
