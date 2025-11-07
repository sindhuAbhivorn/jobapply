from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply, name='apply'),
    path('applicants/', views.admin_applicant_list, name='admin_applicant_list'),
]