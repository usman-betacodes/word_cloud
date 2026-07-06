import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 1. Hit your local API to get the processed data
url = "http://localhost:8084/word-frequency/?max_words=50"
payload = {
    "text": "Bhai kya haal hai, aaj kal AI aur machine learning bohat popular ho gaye hain. naya ai model bohat zabardast kaam kar raha hai. ye system bohat acha hai."
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
        
        # 2. Generate the visual cloud from the frequencies dictionary
        # We set background color to white for better visibility
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            colormap='viridis'
        ).generate_from_frequencies(frequencies)
        
        # 3. Display the image on your screen
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off") # Hide the axes
        plt.tight_layout(pad=0)
        plt.show()
else:
    print(f"API Error: {response.status_code}")
    print(response.text)