from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Applicant

def apply(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        education = request.POST.get('education')
        graduation_year = request.POST.get('graduation_year')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        job_role = request.POST.get('job_role')
        current_company = request.POST.get('current_company')
        expected_salary = request.POST.get('expected_salary')
        notice_period = request.POST.get('notice_period')
        relocate = request.POST.get('relocate')
        referral_code = request.POST.get('referral_code')
        resume = request.FILES.get('resume')

        # Validate required fields
        if not all([full_name, gender, dob, email, phone, address, education,
                    graduation_year, skills, experience, resume, job_role,
                    relocate, referral_code]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('apply')

        # Check for duplicate email or referral code
        if Applicant.objects.filter(email=email).exists():
            messages.error(request, "An application with this email already exists.")
            return redirect('apply')

        if Applicant.objects.filter(referral_code=referral_code).exists():
            messages.error(request, "Referral code already used.")
            return redirect('apply')

        # Save applicant
        Applicant.objects.create(
            full_name=full_name,
            gender=gender,
            dob=dob,
            email=email,
            phone=phone,
            address=address,
            education=education,
            graduation_year=graduation_year,
            skills=skills,
            experience=experience,
            resume=resume,
            job_role=job_role,
            current_company=current_company or None,
            expected_salary=expected_salary or None,
            notice_period=notice_period or None,
            relocate=relocate,
            referral_code=referral_code
        )

        messages.success(request, "Your application has been submitted successfully!")
        return redirect('apply')

    return render(request, 'jobapply.html')


def error_404(request, exception):
    return render(request, '404.html')


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .models import EmailOTP
import datetime
import random

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            otp_obj, created = EmailOTP.objects.get_or_create(email=email)
            otp_obj.otp = str(random.randint(100000, 999999))
            otp_obj.created_at = timezone.now()
            otp_obj.save()

            send_mail(
                subject="Your Login OTP",
                message=f"Your OTP is {otp_obj.otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            request.session['email'] = email
            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')
    return render(request, 'login.html')


def verify_otp_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    
    if request.method == "POST":
        otp_input = request.POST.get('otp')
        try:
            otp_obj = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            messages.error(request, "Invalid session.")
            return redirect('login')
        
        # OTP valid for 5 minutes
        if otp_obj.otp == otp_input and timezone.now() - otp_obj.created_at < datetime.timedelta(minutes=5):
            messages.success(request, "OTP verified successfully.")
            return redirect('admin_applicant_list')  # ✅ Goes to your admin.html page
        else:
            messages.error(request, "Invalid or expired OTP.")
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')


def admin_applicant_list(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')  # Only logged-in users can see admin page

    applicants = Applicant.objects.all().order_by('-submitted_at')
    return render(request, 'admin.html', {'applicants': applicants, 'email': email})


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')