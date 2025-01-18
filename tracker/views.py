from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import JobApplication, Resume
from django.contrib import messages

def dashboard(request):
    recent_applications = JobApplication.objects.all().order_by('-date_applied')[:5]
    upcoming_followups = JobApplication.objects.filter(
        next_follow_up__isnull=False
    ).order_by('next_follow_up')[:5]
    
    context = {
        'recent_applications': recent_applications,
        'upcoming_followups': upcoming_followups,
    }
    return render(request, 'tracker/dashboard.html', context)

def job_list(request):
    jobs = JobApplication.objects.all().order_by('-date_applied')
    return render(request, 'tracker/job_list.html', {'jobs': jobs})

def job_detail_partial(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'tracker/partials/job_detail.html', {'job': job})