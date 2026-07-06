import requests

url = "http://localhost:8084/word-frequency/?max_words=10"
payload = {
  "text": "Pakistan ki economy is improving but inflation bohat zyada hai. پاکستان کی معیشت بہتر ہو رہی ہے."
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
  print("Success! Frequencies:")
  print(response.json())
else:
  print(f"Failed with status code: {response.status_code}")
  print(response.text)
