import json
import ast
import requests
from .fetch_courses import fetch_courses
import google.generativeai as genai
import os
import re
import ast

def new_function():
  skill = "AI ML"
  current_skill_level = "Beginner"
  target_skill_level = "Expert"
  price = "Free"
  genai.configure(api_key="AIzaSyBzjohOuPQSaNZ9hTJBYCiKLwpC_8_PSMo")

  model = genai.GenerativeModel('gemini-1.5-flash')
  
  roadmap_prompt = f"""
  Create a comprehensive roadmap for mastering the topic {skill}, I am currently at {current_skill_level} level and want to get to the level of {target_skill_level}. Provide the output in different levels of increasing difficulty starting from ("Level 1") to maximum ("Level 6") and give the output in a JSON file: Keep the topics as concise as possible, topics should be the main things to learn. A level should no contain more than 5 topics within itself. Ensure the topics are completely technical to help me optimally prepare for my job. Do not include any other text or explanations as well as do not include any text formatting.
  """

  roadmap = model.generate_content(roadmap_prompt).text.replace("`", "").replace("json", "")
  # roadmap = json.loads(roadmap)
  roadmap_dict = ast.literal_eval(roadmap)

  courses = {}

  # fetch_coures
  for level, topics in roadmap_dict.items():
    courses[level] = {}
    for topic in topics:
      courses[level][topic] = fetch_courses(topic, price)