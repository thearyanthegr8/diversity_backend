from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ast
import requests
from .fetch_courses import fetch_courses
import google.generativeai as genai
import os

@csrf_exempt 
def generate_roadmap(request):
  if request.method == "GET":
    skill = request.GET.get('skill', None)
    skill_level = request.GET.get('skill_level', None)
    price = request.GET.get('price', None)
    if skill is None:
      return JsonResponse({'error': 'Skill not provided'}, status=400)
    if skill_level is None:
      return JsonResponse({'error': 'Skill level not provided'}, status=400)

    genai.configure(api_key="AIzaSyBzjohOuPQSaNZ9hTJBYCiKLwpC_8_PSMo")

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    roadmap_prompt = f"""
    Create a comprehensive roadmap for mastering {skill}, structured from complete beginner to a decent level of proficiency, starting from level 1. Provide the answer in bullet points in the following format:
    $$$ Level 1
      !!! Name of Topic 1
        ### Sub Topic 1
        ### Sub Topic 2
        ### Sub Topic 3
      !!! Name of Topic 2
        ### Sub Topic 1
        ### Sub Topic 2
        ### Sub Topic 3
      !!! Name of Topic 3
        ### Sub Topic 1
        ### Sub Topic 2
        ### Sub Topic 3
    And so on...
    Keep the topics concise, topics should be the main things to learn. Don't provide a lot of information. Only the names of the topics and sub-topics are required.
    Do not include any other text or explanations.
    """

    roadmap_response = model.generate_content(roadmap_prompt).text

    levels = roadmap_response.split("$$$")
    levels = [level for level in levels if level.strip()]
    roadmap = {}
    courses = {}

    # To conver into dict
    for i in levels:
      level = i.split("!!!")
      level_name = level[0].strip()
      roadmap[level_name] = {}
      topics = level[1:]
      topics = [topic for topic in topics if topic.strip()]
      for j in topics:
        topic = j.split("###")
        topic_name = topic[0].strip()
        roadmap[level_name][topic_name] = [sub_topic.strip() for sub_topic in topic[1:]]
    
    # fetch_coures
    for level, topics in roadmap.items():
      courses[level] = {}
      for topic in topics:
        courses[level][topic] = fetch_courses(topic, price)

    def convert_to_bullet_points(data):
      result = []
      for level, topics in data.items():
        result.append(f"$$$ {level}")
        for topic, courses in topics.items():
          result.append(f"  !!! {topic}")
          for course in courses:
            result.append(f"   ### {course['title']}")
            result.append(f"    URL: {course['url']}")
            result.append(f"    Description: {course['description']}")
      return "\n".join(result)

    list_courses = convert_to_bullet_points(courses)

    select_courses_prompt = f"""
    You have a list of courses with levels and topics {list_courses}. For each topic, you have a list of courses. The list contains levels, topics, and then courses for each topic. Don't change topic, or the level. Only choose between the couses available for it. Choose the most relevant course for each topic based on title and description. Choose only one course per topic. Format the result as follows:
    $$$ Level 1
      !!! Name of topic 1
        ### Course URL
      !!! Name of topic 2
        ### Course URL
    Include the best course for each topic as specified, and make sure to cover all topics listed. Only provide the formatted data without additional explanations. Don't include any text other than the list. 
    """

    select_courses_response = model.generate_content(select_courses_prompt).text

    # Write output to file
    with open('roadmap_output.txt', 'w') as file:
      file.write("### Roadmap Response\n")
      file.write(roadmap_response + "\n\n")
      file.write("### Roadmap JSON\n")
      file.write(json.dumps(roadmap, indent=2) + "\n\n")
      file.write("### Courses JSON\n")
      file.write(json.dumps(courses, indent=2) + "\n\n")
      file.write("### List of Courses\n")
      file.write(list_courses + "\n\n")
      file.write("### Selected Courses Response\n")
      file.write(select_courses_response + "\n")

    return HttpResponse(
      select_courses_response,
      content_type="application/json"
    )


def generate_interview_questions(request):
  if request.method == "GET":
    skill = request.GET.get('skill', None)
    skill_level = request.GET.get('skill_level', None)
    if skill is None:
      return JsonResponse({'error': 'Skill not provided'}, status=400)

    if skill_level is None:
      return JsonResponse({'error': 'Skill level not provided'}, status=400)

    interview_prompt = f"""
    Create a comprehensive set of 10 questions for {skill}, for someone with a skill of {skill_level}. Do not include any other text or explanations. The questions should only include things one can be asked in an interview. Questions should not have an option to write the code. Some of the coding question's 
    """

    # return HttpResponse(
    #   interview_response,
    #   content_type="application/json"
    # )