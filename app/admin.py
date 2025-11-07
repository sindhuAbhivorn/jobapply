from django.contrib import admin
from .models import Applicant,EmailOTP
# Register your models here.
admin.site.register(Applicant)
admin.site.register(EmailOTP)