from django.db import models
from django.utils import timezone

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    date_applied = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    job_description = models.TextField(blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    next_follow_up = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company_name}"

class Communication(models.Model):
    job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='communications')
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=50)  # email, phone, interview, etc.
    notes = models.TextField()

    class Meta:
        ordering = ['-date']

class Resume(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_master = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)