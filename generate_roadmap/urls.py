from django.urls import path
from . import views

urlpatterns = [
  path('generate-roadmap/', views.generate_roadmap, name='hello')
]