from django.db import models

# Create your models here.

class Job(models.Model):
    location = models.TextField()
    job_title = models.CharField(max_length=100)
    level = models.TextField()
    corporate = models.TextField()
    requirements = models.TextField()