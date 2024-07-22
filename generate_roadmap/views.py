from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def generate_roadmap(request):
  return HttpResponse("Hello world!")