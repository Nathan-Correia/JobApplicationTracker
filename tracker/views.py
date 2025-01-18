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
    if request.method == 'POST':
    # Create the job from posted data (handle validation, etc.)
        job = JobApplication.objects.create(
            company_name=request.POST.get('company_name'),
            position=request.POST.get('position'),
            date_applied=request.POST.get('date_applied') or None,
            status=request.POST.get('status'),
            job_description=request.POST.get('job_description', ''),
            salary_range=request.POST.get('salary_range', ''),
            next_follow_up=request.POST.get('next_follow_up') or None,
            notes=request.POST.get('notes', ''),
        )
        # Render partial row for this new job
        return render(request, 'tracker/partials/add_item.html', {'job': job})
    return render(request, 'tracker/partials/add_item.html')

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

def actually_add_job(request):
    if request.method == 'POST':
        # Retrieve data from request.POST (a QueryDict)
        company_name = request.POST.get('company_name')
        position = request.POST.get('position')
        date_applied = request.POST.get('date_applied')
        status = request.POST.get('status')
        job_description = request.POST.get('job_description')
        salary_range = request.POST.get('salary_range')
        next_follow_up = request.POST.get('next_follow_up')
        notes = request.POST.get('notes')

    # Convert date strings to Python date objects if necessary
    if date_applied:
        date_applied = timezone.datetime.strptime(date_applied, '%Y-%m-%d').date()
    if next_follow_up:
        next_follow_up = timezone.datetime.strptime(next_follow_up, '%Y-%m-%d').date()

    # Create a new JobApplication object
    JobApplication.objects.create(
        company_name=company_name,
        position=position,
        date_applied=date_applied,
        status=status,
        job_description=job_description,
        salary_range=salary_range,
        next_follow_up=next_follow_up,
        notes=notes
    )


    jobs = JobApplication.objects.all()

    return render(request, 'tracker/partials/main_table.html', {'jobs': jobs})

def get_table_again(request):
    jobs = JobApplication.objects.all()

    return render(request, 'tracker/partials/main_table.html', {'jobs': jobs})
