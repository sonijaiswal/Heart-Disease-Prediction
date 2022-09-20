import requests
from requests.auth import HTTPBasicAuth

login_url = 'http://localhost:8000/api/users/token/'


requests.post(login_url, auth=HTTPBasicAuth('admin', 'admin'))

url = 'http://localhost:8000/api/hearts'

response = requests.get(url)

print(response)
