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
    title = i["title"]
    url = f"https://www.udemy.com{i['url']}"
    description = i["headline"]
    thumbnail = i["image_480x270"]
    price = i["price"]
    videos.append({"title": title, "url": url, "description": description, "thumbnail": thumbnail, "price": price})

  return videos