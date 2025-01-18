from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import JobApplication, Resume, Communication
from django.utils import timezone
from django import forms
from django.urls import reverse

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['company_name', 'position', 'date_applied', 'status', 
                 'job_description', 'salary_range', 'next_follow_up', 'notes']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
            'next_follow_up': forms.DateInput(attrs={'type': 'date'}),
            'job_description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = ['type', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content', 'is_master']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 20}),
        }

def main_landing(request):
    return render(request, 'tracker/default_page.html')

def dashboard(request):
    recent_applications = JobApplication.objects.all().order_by('-date_applied')[:5]
    upcoming_followups = JobApplication.objects.filter(
        next_follow_up__isnull=False
    ).order_by('next_follow_up')[:5]
    
    total_applications = JobApplication.objects.count()
    active_applications = JobApplication.objects.exclude(
        status__in=['rejected', 'accepted']
    ).count()
    
    status_counts = {
        status: JobApplication.objects.filter(status=status[0]).count()
        for status in JobApplication.STATUS_CHOICES
    }
    
    context = {
        'recent_applications': recent_applications,
        'upcoming_followups': upcoming_followups,
        'total_applications': total_applications,
        'active_applications': active_applications,
        'status_counts': status_counts,
    }
    return render(request, 'tracker/dashboard.html', context)

def job_list(request):
    jobs = JobApplication.objects.all().order_by('-date_applied')
    return render(request, 'tracker/job_list.html', {'jobs': jobs})

def job_detail_partial(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'tracker/job_detail.html', {'job': job})

@require_http_methods(["GET", "POST"])
def job_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(reverse('job_list'))
        return render(request, 'tracker/job_form.html', {'form': form, 'title': 'Add New Job Application'})
    else:
        form = JobApplicationForm()
    return render(request, 'tracker/job_form.html', {'form': form, 'title': 'Add New Job Application'})

@require_http_methods(["GET", "POST"])
def job_edit(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(reverse('job_list'))
        return render(request, 'tracker/job_form.html', {'form': form, 'title': f'Edit Job Application: {job.position}'})
    else:
        form = JobApplicationForm(instance=job)
    return render(request, 'tracker/job_form.html', {'form': form, 'title': f'Edit Job Application: {job.position}'})

@require_http_methods(["GET", "POST"])
def communication_create(request, job_pk):
    job = get_object_or_404(JobApplication, pk=job_pk)
    if request.method == "POST":
        form = CommunicationForm(request.POST)
        if form.is_valid():
            communication = form.save(commit=False)
            communication.job_application = job
            communication.save()
            return HttpResponseRedirect(reverse('job_detail_partial', args=[job_pk]))
    else:
        form = CommunicationForm()
    return render(request, 'tracker/communication_form.html', {'form': form, 'job': job})

def resume_list(request):
    resumes = Resume.objects.all().order_by('-updated_at')
    return render(request, 'tracker/resume_list.html', {'resumes': resumes})

@require_http_methods(["GET", "POST"])
def resume_create(request):
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            if resume.is_master:
                Resume.objects.filter(is_master=True).update(is_master=False)
            resume.save()
            return HttpResponseRedirect(reverse('resume_list'))
    else:
        form = ResumeForm()
    return render(request, 'tracker/resume_form.html', {'form': form})

def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            resume = form.save(commit=False)
            if resume.is_master:
                Resume.objects.filter(is_master=True).exclude(pk=resume.pk).update(is_master=False)
            resume.save()
            return HttpResponseRedirect(reverse('resume_list'))
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'tracker/resume_form.html', {'form': form, 'resume': resume})