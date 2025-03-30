from django.contrib import admin

# Register your models here.
from .models import Job

admin.site.register(Job)
class JobAdmin(admin.ModelAdmin):
    #customise admin display
    list_display = ('title','description','link')