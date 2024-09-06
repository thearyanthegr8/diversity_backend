from django.urls import path
from . import views
from .views import score_answers

urlpatterns = [
  path('generate-roadmap/', views.generate_roadmap),
  path('generate-mcqs/', views.generate_mcqs),
  path('generate-interview-questions/', views.generate_interview_questions),
  path('score/', score_answers, name='score_answers')
]