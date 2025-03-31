from django.db import models

# Create your models here.
class Job(models.Model):
    #Title of the project
    title = models.CharField(max_length=200)
    #description of the project
    description = models.TextField()
    #link to view projects if any
    link = models.URLField(blank=True,null=True)
    #image for the project
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title

