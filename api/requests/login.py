import requests
import json
from requests.auth import HTTPBasicAuth


login_url = 'http://localhost:8000/api/users/token/'


requests.post(login_url, auth=HTTPBasicAuth('admin', 'admin'))

# refresh = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NjI4NzU4MywiaWF0IjoxNjYzNjk1NTgzLCJqdGkiOiJkZjY1MTM2NDBiM2I0Y2E3YWMxYTk2YmE4MmY2MWIxYSIsInVzZXJfaWQiOjF9.qzbqzNvs7i5GG94W61QP37on5KFuitkTjnwLgcJzH-c",
# access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzNzgxOTgzLCJpYXQiOjE2NjM2OTU1ODMsImp0aSI6IjJhZjI5MzBkMzkzMzQ2NzFhNmJiNWQxZTlhM2ZjNWFjIiwidXNlcl9pZCI6MX0.cyKcp-dnKzzNJPVvR4ZZ2TGcJYg5_NUzbm6sUeSAE-4"


# head = {'Authorization': 'Bearer {}'.format(access)}


# response = requests.post(url = url,headers=head)

# print(response.text )

