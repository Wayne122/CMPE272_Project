from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class userRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=[('PO', 'Project Owner'), ('EX', 'Expert'), ('AM', 'Ambassador')])


def validate_file_ext(value):
    if os.path.splitext(os.path.basename(value.name))[1] != '.pdf':
        raise ValidationError("Please upload pdf files only.")
    else:
        return value


class whitePaper(models.Model):
    WPFile = models.FileField(validators=[validate_file_ext])
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True)
    dueTime = models.DateTimeField()
    uploadTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, related_name='uploader', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    acceptor = models.ForeignKey(User, related_name='acceptor', on_delete=models.CASCADE, null=True, blank=True)


class videos(models.Model):
    video_url = models.URLField()
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True)
    uploadTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    WP = models.ForeignKey(whitePaper, on_delete=models.CASCADE)


class testQuestions(models.Model):
    q1 = models.TextField()
    a1 = models.TextField()
    a2 = models.TextField()
    a3 = models.TextField()
    a4 = models.TextField()
    CA = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    WP = models.ForeignKey(whitePaper, on_delete=models.CASCADE)
