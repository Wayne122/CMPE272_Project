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
    dueTime = models.DateField()
    uploadTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, related_name='uploader', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    acceptor = models.ForeignKey(User, related_name='acceptor', on_delete=models.CASCADE, null=True, blank=True)


class wpClass(models.Model):
    video_url = models.URLField()
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True)
    uploadTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    WP = models.ForeignKey(whitePaper, on_delete=models.CASCADE)


class wpQuiz(models.Model):
    q1 = models.TextField()
    q1a1 = models.TextField()
    q1a2 = models.TextField()
    q1a3 = models.TextField()
    q1a4 = models.TextField()
    q1ans = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    q2 = models.TextField()
    q2a1 = models.TextField()
    q2a2 = models.TextField()
    q2a3 = models.TextField()
    q2a4 = models.TextField()
    q2ans = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    q3 = models.TextField()
    q3a1 = models.TextField()
    q3a2 = models.TextField()
    q3a3 = models.TextField()
    q3a4 = models.TextField()
    q3ans = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    q4 = models.TextField()
    q4a1 = models.TextField()
    q4a2 = models.TextField()
    q4a3 = models.TextField()
    q4a4 = models.TextField()
    q4ans = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    q5 = models.TextField()
    q5a1 = models.TextField()
    q5a2 = models.TextField()
    q5a3 = models.TextField()
    q5a4 = models.TextField()
    q5ans = models.CharField(max_length=1, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    WP = models.ForeignKey(whitePaper, on_delete=models.CASCADE)