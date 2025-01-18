from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_landing, name='main_landing'),
    path('add_job_list', views.add_job_list, name='add_job_list'),
    path('refresh_job_list', views.refresh_job_list, name='refresh_job_list'),
    path('delete/', views.delete_individual, name='delete_individual'),
    path('application/<int:application_id>/details', views.application_details, name='application_details'),
    path('application/<int:application_id>/view', views.application_view, name='application_view'),
    path('application/<int:application_id>/edit', views.edit, name='edit'),
    path('application/<int:application_id>/update', views.update_application, name='update'),
    path('main/page', views.get_table_again, name='main_page'),
    path('actually_add_job', views.actually_add_job, name='actually_add_job'),
    path('resume/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:resume_id>/customize/', views.customize_resume, name='customize_resume'),
    path('resume/custom/<int:resume_id>/', views.custom_resume_detail, name='custom_resume_detail')
]