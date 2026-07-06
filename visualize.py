import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud

url = "http://localhost:8084/word-frequency/?max_words=50"
payload = {
  "text": (
    "Pakistan ki economy is improving but inflation bohat zyada hai. "
    "Bhai kya haal hai, aaj kal AI aur machine learning bohat popular ho gaye hain."
  )
}

print("Fetching data from API...")
response = requests.post(url, json=payload)

if response.status_code == 200:
  data = response.json()
  frequencies = data.get("frequencies", {})

  if not frequencies:
    print("No valid words found to visualize.")
  else:
    print(f"Generating Word Cloud for: {frequencies}")
    wordcloud = WordCloud(
      width=800,
      height=400,
      background_color="white",
      colormap="viridis",
    ).generate_from_frequencies(frequencies)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
else:
  print(f"API Error: {response.status_code}")
  print(response.text)
