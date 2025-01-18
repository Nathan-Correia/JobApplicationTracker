from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_landing, name='dashboard'),
    path('resume/create/', views.create_resume, name='create_resume'),
    path('resume/<int:resume_id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:resume_id>/customize/', views.customize_resume, name='customize_resume'),
    path('resume/custom/<int:resume_id>/', views.custom_resume_detail, name='custom_resume_detail'),

]