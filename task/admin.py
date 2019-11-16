from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import whitePaper, videos, testQuestions, userRole

# Register your models here.

admin.site.register(whitePaper)
admin.site.register(videos)
admin.site.register(testQuestions)

class userRoleInline(admin.StackedInline):
    model = userRole
    can_delete = False
    verbose_name_plural = 'userRole'

class UserAdmin(BaseUserAdmin):
    inlines = (userRoleInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)