from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import JobApplication, Resume, Communication
from django.utils import timezone
from django import forms
from django.urls import reverse
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
    return render(request, 'tracker/default_page.html')

def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            print("valid")
            resume = form.save()
            resume.user = "1"
            resume.save()
            return redirect('resume_detail', resume_id=resume.id)  # Redirect with the correct id
        else:
            print("invalid")
    else:
        form = ResumeForm()
    return render(request, 'tracker/resume_form.html', {'form': form})


def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect(reverse('resume_detail', args=[resume.id]))
    else:
        form = ResumeForm(instance=resume)
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
