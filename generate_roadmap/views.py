from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from langchain_community.llms import Ollama
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt 
def generate_roadmap(request):
  if request.method == "POST":
    data = json.loads(request.body)
    skill = data.get('skill', None)
    if skill is None:
            return JsonResponse({'error': 'Skill not provided'}, status=400)
    
    llm = Ollama(model="llama3:8b", base_url="http://localhost:11434")
    roadmap_prompt = f"Create a detailed, topic-wise roadmap for mastering {skill}, structured from beginner to advanced levels. List the key topics and subtopics in a logical sequence for someone starting from scratch. Provide the output in bullet points, using only headings and subheadings without sentences."

    response = llm.invoke(roadmap_prompt)
    return HttpResponse(response)