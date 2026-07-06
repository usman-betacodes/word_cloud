import requests

url = "http://localhost:8084/word-frequency/?max_words=10"
payload = {
    "text": "ye naya model bohat tez hai aur aik acha system hai"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    print("Success! Frequencies:")
    print(response.json())
else:
    print(f"Failed with status code: {response.status_code}")
    print(response.text)