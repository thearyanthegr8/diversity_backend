from langchain_community.llms import Ollama
from langchain_chroma import Chroma
# from quiz_data import questions
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from quiz_data import questions
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_core.documents import Document
# from langchain_community import embeddings
from langchain_ollama import OllamaEmbeddings
from similar_neighbours import similar_neighbours

load_dotenv()
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1024, chunk_overlap=20, length_function=len
)
folder_path = "db"

# llm = Ollama(model="llama3.1:8b")
genai.configure(api_key=os.getenv("GENERATIVE_API_KEY"))
gemini = genai.GenerativeModel('gemini-1.5-flash')

embeddings = OllamaEmbeddings(
    model="llama3.1:8b",
)

# # How to Generate using Gemini:
# response = gemini.generate_content("Tell me a joke")
# # How to Generate using LLM:
# response = llm.invoke("What is the difference between an array and a linked list?")

async def scrape_site(site):
  data = ""
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)

    page = await browser.new_page()
    await page.goto(site)

    page_source = await page.content()
    soup = BeautifulSoup(page_source, 'html.parser')

    for script in soup(["script", "style"]):
      script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    data = '\n'.join(chunk for chunk in chunks if chunk)

    await browser.close()
  return data

async def search_scrape(question):
  links = []
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto(f"https://www.google.com/search?q={question}")
    page_source = await page.content()
    soup = BeautifulSoup(page_source, 'html.parser')

    for link in soup.find_all("a"):
      href = link.get("href")
      if href and href.startswith("https://") and "google.com" not in href and ".pdf" not in href:
        links.append(href)

    await browser.close()
  return links



# vector_store.add_documents(
#   google_data
# )

def grading(arr, user_ss, selected_ss):
  if user_ss == selected_ss:
    return 1
  else:
    mean = sum(arr) / len(arr)
    stddev = (sum((x - mean) ** 2 for x in arr) / len(arr)) ** 0.5
    z = (user_ss - mean) / stddev

    print("Z Score: ", z)

    if (z >= 1):
      print("A+")
      return "A+"
    elif (z >= 0.5 and z < 1):
      print("A")
      return "A"
    elif (z >= 0 and z < 0.5):
      print("B")
      return "B"
    elif (z >= -0.5 and z < 0):
      print("C")
      return "C"
    elif (z >= -1 and z < -0.5):
      print("D")
      return "D"
    else:
      print("F")
      return "F"

    # for res, score in ss:
    #   print(score)
    #   similarity_scores.append(score)

def ai_main(questions):
  for question in questions:
    ss = 0
    similarity_scores = []
    answers = []

    output = asyncio.run(search_scrape(question["question"]))
    website_data = []
    for i in range(5):
      website_data.append(asyncio.run(scrape_site(output[0])))

    website_data_str = " ".join(website_data)
    # website_data_chroma = text_splitter.split_text(website_data_str)

    google_data = [Document(
      page_content=website_data_str,
      id=1
    )]

    vector_store = Chroma.from_documents(
        documents=google_data,
        collection_name="question",
        embedding=embeddings,
    )

    while(similar_neighbours(similarity_scores) == -1):
      # output = asyncio.run(scrape_site("https://www.futuretools.io/"))
      gemini_answer = gemini.generate_content(question["question"])

      # llm_data = [Document(
      #   page_content=gemini_answer.text,
      #   id=2
      # )]

      # vector_store.add_documents(
      #   llm_data
      # )

      # Check Similarity Score
      ss = vector_store.similarity_search_with_score(gemini_answer.text, k=2)
      print(similarity_scores)
      print(ss[-1][1])
      similarity_scores.append(ss[-1][1])
      answers.append({
        "answer": gemini_answer.text,
        "score": ss[-1][1]
      })

    selected_similarity_score = similar_neighbours(similarity_scores)
    print("Selected Similarity Score: ", selected_similarity_score)
    selected_answer = next(answer["answer"] for answer in answers if answer["score"] == selected_similarity_score)
    print("Selected Answer: ", selected_answer)

    gemini_data = [Document(
      page_content=selected_answer,
      id=1
    )]

    vector_store = Chroma.from_documents(
      documents=gemini_data,
      collection_name="user_answer",
      embedding=embeddings,
    )

    user_ss = vector_store.similarity_search_with_score(question["answer"], k=2)
    # Fix this later
    print("User SS: ", user_ss[-1][1])

    return grading(similarity_scores, user_ss[-1][1] + 0.4, selected_similarity_score)