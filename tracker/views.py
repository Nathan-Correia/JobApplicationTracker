from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import JobApplication, Resume, Communication
from django.utils import timezone
from django import forms
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Resume
from django.forms.models import model_to_dict


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'full_name',
            'contact_email',
            'phone_number',
            'address',
            'summary',
            'work_experience',
            'education',
            'skills',
            'projects',
            'additional_info',
        ]
        widgets = {
            'work_experience': forms.Textarea(attrs={'rows': 5}),
            'education': forms.Textarea(attrs={'rows': 5}),
            'projects': forms.Textarea(attrs={'rows': 5}),
            'additional_info': forms.Textarea(attrs={'rows': 5}),
        }

        
def main_landing(request):
    jobs = JobApplication.objects.all()
    return render(request, 'tracker/main_landing.html', {'jobs': jobs})

def add_job_list(request):
    import random
    from datetime import timedelta, date
    from tracker.models import JobApplication

    # Helper function to generate random dates
    def random_date(start, end):
        delta = end - start
        random_days = random.randint(0, delta.days)
        return start + timedelta(days=random_days)

    # Data for generating random objects
    companies = ["TechCorp", "DataWorks", "DesignCo", "InnoSoft", "HealthPlus"]
    positions = ["Software Engineer", "Data Scientist", "UX Designer", "Product Manager", "System Analyst"]
    statuses = ["applied", "screening", "interview", "offer", "rejected", "accepted"]
    descriptions = [
        "Develop and maintain software solutions.",
        "Analyze datasets and build predictive models.",
        "Design user-friendly interfaces and experiences.",
        "Manage product development lifecycles.",
        "Optimize IT systems for scalability and efficiency.",
    ]
    salary_ranges = ["$60k - $80k", "$70k - $90k", "$80k - $110k", "$90k - $120k", "$100k - $130k"]

    # Generate random objects
    start_date = date(2023, 1, 1)
    end_date = date(2025, 1, 1)

    for i in range(10):  # Create 10 objects
        JobApplication.objects.create(
            company_name=random.choice(companies),
            position=random.choice(positions),
            date_applied=random_date(start_date, end_date),
            status=random.choice(statuses),
            job_description=random.choice(descriptions),
            salary_range=random.choice(salary_ranges),
            next_follow_up=random_date(date.today(), date.today() + timedelta(days=30)),
            notes=f"Sample note for job application {i + 1}.",
        )

    return render(request, 'tracker/partials/job_table.html')

def refresh_job_list(request):

    jobs = JobApplication.objects.all()


    return render(request, 'tracker/partials/job_table.html', {'jobs': jobs})

@csrf_exempt
def application_details(request, application_id):
    job = get_object_or_404(JobApplication, id=int(application_id))
    return render(request, 'tracker/partials/application_details.html', {'job': job})

def application_view(request, application_id):
    return HttpResponse(status=200)

@csrf_exempt  # Disable CSRF for simplicity in this view
@require_http_methods(["DELETE"])
def delete_individual(request):
    job_id = request.headers.get('X-Job-ID', None)

    if not job_id:
        return HttpResponse(status=400)  # Bad Request if no job ID

    job = get_object_or_404(JobApplication, id=int(job_id))
    job.delete()

    # Return a 204 No Content response to remove the row
    return HttpResponse(status=200)

def edit_resume(request):
    resume = Resume.objects.filter(user="1").first()
    edit = request.GET.get('edit', 'false').lower() == 'true'

    if request.method == 'POST':
        # Handle form submission (create or update resume)
        form = ResumeForm(request.POST, instance=resume if resume else None)
        if form.is_valid():
            resume = form.save()
            return redirect(reverse('resume_detail', args=[resume.id]))
    else:
        # Handle form display (edit or create mode)
        if edit and resume:
            form = ResumeForm(instance=resume)  # Populate form with existing resume data
        elif resume:
            return redirect(reverse('resume_detail', args=[resume.id]))  # Redirect if not in edit mode
        else:
            form = ResumeForm()  # Empty form for new resume

    return render(request, 'tracker/resume_form.html', {'form': form})

def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, 'tracker/resume_detail.html', {'resume': resume})


def customize_resume(request, resume_id):
    # https://stackoverflow.com/a/65640286
    resume = Resume.objects.get(pk=resume_id)
    data = model_to_dict(resume)
    data.pop('id', None)
    custom_resume = Resume.objects.create(**data)
    custom_resume.user = None
    custom_resume.save()
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=custom_resume)
        if form.is_valid():
            resume = form.save()
            return redirect('custom_resume_detail', resume_id=resume.id)  # Redirect to the detail view
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'tracker/resume_form.html', {'form': form})

def custom_resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, 'tracker/custom_resume_detail.html', {'resume': resume})
