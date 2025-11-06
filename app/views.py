from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Applicant

def apply_view(request):
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
        if not all([full_name, gender, dob, email, phone, address, education, graduation_year, skills, experience, resume, job_role, relocate, referral_code]):
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
