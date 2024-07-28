import requests

def fetch_courses(topic, price):
    udemy_price = "price-paid" if price == "paid" else "price-free" if price == "free" else ""
    videos = []
    udemy_url = f"https://www.udemy.com/api-2.0/courses/?page_size=3&search={topic}&ordering=relevance&language=en"
    if udemy_price:
        udemy_url += f"&price={udemy_price}"
    r = requests.get(udemy_url, headers={
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Basic eXpJb3UyTEFnbzU0UVN0N3hMaHBnOWxTTThiTnc4dnNWMDhORlFuTToxMjQxTnRFZkNnWEJodXJYUFZ4YkhjZlB6a0xObXJpY2FFMXB6Z1piQldqVmZvaDA0WlYxYzVzRVNGRHlGNHlQaUJrUXpEMHpKZGdMbkpJWDE3QlQ5OTBKZHZPMzNNR01CREozSkRpQ29VRnpKSFVqWXdWb1NrNUtDQ0Fpa0Y4ag==",
        "Content-Type": "application/json"
    })

    for i in r.json()["results"]:
        id = i["id"]
        title = i["title"]
        url = f"https://www.udemy.com{i['url']}"
        description = i["headline"]
        thumbnail = i["image_480x270"]
        price = i["price"]
        course_structure = fetch_course_structure(id)
        videos.append({
            "id": id,
            "title": title,
            "url": url,
            "description": description,
            "thumbnail": thumbnail,
            "price": price,
            "course_structure": course_structure
        })

    return videos

def fetch_course_structure(id):
    url = f"https://www.udemy.com/api-2.0/courses/{id}/public-curriculum-items/?page_size=10000"
    response = requests.get(url, headers={
        "Accept": "application/json, text/plain, */*",
        "Authorization": "Basic eXpJb3UyTEFnbzU0UVN0N3hMaHBnOWxTTThiTnc4dnNWMDhORlFuTToxMjQxTnRFZkNnWEJodXJYUFZ4YkhjZlB6a0xObXJpY2FFMXB6Z1piQldqVmZvaDA0WlYxYzVzRVNGRHlGNHlQaUJrUXpEMHpKZGdMbkpJWDE3QlQ5OTBKZHZPMzNNR01CREozSkRpQ29VRnpKSFVqWXdWb1NrNUtDQ0Fpa0Y4ag==",
        "Content-Type": "application/json"
    })
    
    data = response.json()
    course_structure = {}
    
    current_chapter = None
    
    for item in data["results"]:
        if item["_class"] == "chapter":
            current_chapter = item["title"]
            course_structure[current_chapter] = []
        elif item["_class"] == "lecture" and current_chapter:
            course_structure[current_chapter].append(item["title"])
    
    return course_structure

# url = "https://www.udemy.com/api-2.0/courses/950390/public-curriculum-items/?page_size=10000"
# course_structure = fetch_course_structure(url)
# print(course_structure)