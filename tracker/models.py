from django.db import models
from django.utils import timezone
from django.conf import settings


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
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
    # https://stackoverflow.com/a/63255662
    # Resume.objects.filter(user="1")
    user = models.CharField(max_length=255, blank=True, null=True, default="1")

    # Basic Information
    full_name = models.CharField(blank=True, max_length=255)
    contact_email = models.TextField(blank=True)
    phone_number = models.CharField(blank=True, max_length=20)
    address = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    work_experience = models.JSONField(default=list)
    education = models.JSONField(default=list)

    # comma separated
    skills = models.TextField(blank=True)

    projects = models.JSONField(default=list)
    additional_info = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume for {self.full_name}"
    

'''
full_name : Jane Doe
contact_email : janedoe@example.com
phone_number : 555-123-4567
address : 123 Main St, Springfield, IL 62701
summary : Experienced software engineer with a passion for web development and problem-solving. Proficient in Python, Django, and JavaScript.

work_experience : 
[
    {
        "company": "Tech Solutions Inc.",
        "role": "Software Engineer",
        "start_date": "2020-06-01",
        "end_date": "Present",
        "responsibilities": [
            "Developed and maintained web applications using Python and Django.",
            "Collaborated with cross-functional teams to deliver software solutions.",
            "Mentored junior developers and conducted code reviews."
        ]
    },
    {
        "company": "Web Dev Studio",
        "role": "Frontend Developer",
        "start_date": "2018-08-15",
        "end_date": "2020-05-30",
        "responsibilities": [
            "Designed and implemented responsive user interfaces using HTML, CSS, and JavaScript.",
            "Worked with the design team to improve user experience.",
            "Optimized frontend performance for faster load times."
        ]
    }
]

education :
[
    {
        "institution": "Springfield University",
        "degree": "Bachelor of Science in Computer Science",
        "graduation_year": 2018
    }
]

skills : Python, Django, JavaScript, HTML, CSS, React, Git, SQL, REST APIs, Agile methodologies
projects : 
[
    {
        "name": "Personal Portfolio Website",
        "description": "Built a personal portfolio website to showcase projects and technical skills using Django and React."
    },
    {
        "name": "Task Manager App",
        "description": "Developed a task management web application with task prioritization and notification features."
    }
]

additional_info : Fluent in English and Spanish. Open to remote and on-site opportunities.

'''