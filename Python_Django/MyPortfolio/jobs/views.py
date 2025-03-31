from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Job

def jobs(request):
    #fetch all jobs from the database
    jobs=Job.objects.all()
    return render(request,'SamplePortfolio.html',{'jobs':jobs})
#    template = loader.get_template('SamplePortfolio.html')
#    return HttpResponse(template.render())