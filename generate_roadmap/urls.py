from django.urls import path
from . import views

urlpatterns = [
  path('generate-roadmap/', views.test_roadmap),
  path('generate-mcqs/', views.generate_mcqs),
  path('generate-interview-questions/', views.generate_interview_questions)
]