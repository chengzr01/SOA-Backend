from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Job(models.Model):
    location = models.TextField()
    job_title = models.CharField(max_length=100)
    level = models.TextField()
    corporate = models.TextField()
    requirements = models.TextField()

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_user_message = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        sender_type = "user" if self.is_user_message else "system"
        return f"[{sender_type}]: {self.message}"