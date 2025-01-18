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


def edit(request, application_id):
    job = get_object_or_404(JobApplication, id=int(application_id))
    return render(request, 'tracker/partials/application_details_edit.html', {'job': job})

def application_view(request, application_id):
    return HttpResponse(status=200)


@csrf_exempt  # Since you're using HTMX
def update_application(request, application_id):
    job = get_object_or_404(JobApplication, id=application_id)
    
    # Update the fields
    job.company_name = request.POST.get('company_name', job.company_name)
    job.position = request.POST.get('position', job.position) 
    job.salary_range = request.POST.get('salary_range', job.salary_range)
    
    job.save()
    
    # Return the view template with updated job
    return render(request, 'tracker/partials/application_details.html', {'job': job})

@require_http_methods(["DELETE"])
def delete_individual(request):
    job_id = request.headers.get('X-Job-ID', None)

    if not job_id:
        return HttpResponse(status=400)  # Bad Request if no job ID

    job = get_object_or_404(JobApplication, id=int(job_id))
    job.delete()

    # Return a 204 No Content response to remove the row
    return HttpResponse(status=200)
