from django.urls import path
from . import views

urlpatterns = [
  path('generate-roadmap/', views.generate_roadmap),
  path('generate-interview-questions/', views.generate_interview_questions)
]