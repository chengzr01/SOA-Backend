from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Job(models.Model):
    location = models.TextField()
    job_title = models.CharField(max_length=100)
    level = models.TextField()
    corporate = models.TextField()
    requirements = models.TextField()

def validate_sender_or_receiver_exists(sender, receiver, **kwargs):
    if sender is None and receiver is None:
        raise ValidationError("Either sender or receiver must be provided.")

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', blank=True, null=True)
    message = models.TextField()
    is_user_message = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        sender_type = "user" if self.is_user_message else "system"
        return f"[{sender_type}]: {self.message}"

    def clean(self):
        validate_sender_or_receiver_exists(self.sender, self.receiver)


class UserProfile(models.Model):
    pass
    # TODO: Add fields for user profile