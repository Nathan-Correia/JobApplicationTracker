from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_landing, name='main_landing'),
    path('add_job_list', views.add_job_list, name='add_job_list'),
    path('refresh_job_list', views.refresh_job_list, name='refresh_job_list'),
    path('delete/', views.delete_individual, name='delete_individual'),
    path('application/<int:application_id>/details', views.application_details, name='application_details'),
    path('application/<int:application_id>/view', views.application_view, name='application_view')
]