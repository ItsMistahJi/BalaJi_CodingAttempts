from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

def jobs(request):
    template = loader.get_template('SamplePortfolio.html')
    return HttpResponse(template.render())