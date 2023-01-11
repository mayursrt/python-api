import requests

URL = "http://127.0.0.1:8000"

def get_published_posts():
    response = requests.get(f"{URL}/posts/published")
    return response.json()