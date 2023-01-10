import requests
from pydantic import BaseModel, EmailStr


def authenticate_user(username : EmailStr, password : str):
    form_data = {'username': username, 'password': password}
    response = requests.post("http://127.0.0.1:8000/login", data=form_data)
    if response.status_code == 200:
        return True
    else:
        return False
    
def add_user(username : EmailStr, password : str):
    form_data = {'email': username, 'password': password}
    response = requests.post("http://127.0.0.1:8000/users/", json=form_data)
    print(response.json())
    if response.status_code == 201:
        return True
    else:
        return False