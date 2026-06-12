import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzgxNzAzNDQyfQ.pc9hyHKddF6hXpIUlDHJ4BrnES-Ik9CrwbFeOKJcRMM"
}

requisicao = requests.get("http://localhost:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())