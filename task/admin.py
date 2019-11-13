from django.contrib import admin
from .models import whitePaper, videos, testQuestions

# Register your models here.

admin.site.register(whitePaper)
admin.site.register(videos)
admin.site.register(testQuestions)