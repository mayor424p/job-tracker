from django.db import models
from django.conf import settings

class jobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
    ]

    
    SOURCE_CHOICES = [
    ('linkedin', 'LinkedIn'),
    ('company_website', 'Company Website'),
    ('job_board', 'Job Board (e.g., Indeed, Glassdoor)'),
    ('referral', 'Referral'),
    ('career_fair', 'Career Fair'),
    ('other', 'Other'),
    
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    source = models.CharField(max_length=50, choices= SOURCE_CHOICES, blank=True, null=True)
    date_applied = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company} - {self.role} ({self.user})"
    

class StatusHistory(models.Model):
    job = models.ForeignKey(jobApplication, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20, choices=jobApplication.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=jobApplication.STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.job} changed from {self.old_status} to {self.new_status} at {self.changed_at}"
    

class interviewLog(models.Model):
    job = models.ForeignKey(jobApplication, on_delete=models.CASCADE, related_name='interviews')
    interview_date = models.DateTimeField()
    interviewer = models.CharField(max_length=255, blank=True, null=True)
    mode = models.CharField(max_length=100, blank=True, null=True)  # e.g., In-person, Phone, Video
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-interview_date']

    def __str__(self):
        return f"Interview for {self.job} on {self.interview_date}"
    

class ResumeAnalysis(models.Model):
    job = models.ForeignKey(jobApplication, on_delete=models.CASCADE, related_name='resume_analyses')
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    analysis_date = models.DateTimeField(auto_now_add=True)
    job_description = models.TextField(blank=True, null=True)
    match_score = models.FloatField(null = True, blank=True)
    missing_keywords = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-analysis_date']

    def __str__(self):
        return f"Resume Analysis {self.id} for {self.job} on {self.analysis_date} (Score: {self.match_score})"
