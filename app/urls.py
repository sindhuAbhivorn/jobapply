from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('verify/', views.verify_otp_view, name='verify_otp'),
    path('apply/', views.apply, name='apply'),
    path('applicants/', views.admin_applicant_list, name='admin_applicant_list'),
    path('logout/', views.logout_view, name='logout'),
]