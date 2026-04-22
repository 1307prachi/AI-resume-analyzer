from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='resumes/')
    job_description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AnalysisResult(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    score_breakdown = models.JSONField(default=dict)
    matched_keywords = models.JSONField(default=list)
    missing_keywords = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    summary = models.TextField(blank=True)