import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=watches"  # Update the URL for watches

headers = {
    "User-Agent": "Your User Agent String"
}

max_retries = 5
retry_delay = 5  # seconds

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
watch_cards = soup.find_all("div", class_="s-result-item")

watch_data = []

for watch_card in watch_cards:
    try:
        watch_name = watch_card.find("span", class_="a-text-normal").text.strip()
        watch_price = watch_card.find("span", class_="a-offscreen").text if watch_card.find("span", class_="a-offscreen") else "N/A"
        watch_rating = watch_card.find("span", class_="a-icon-alt").text if watch_card.find("span", class_="a-icon-alt") else "N/A"
        
        watch_data.append({
            "Name": watch_name,
            "Price": watch_price,
            "Rating": watch_rating
        })
    except Exception as e:
        print("Error in extracting watch data:", e)

df = pd.DataFrame(watch_data)
df.to_csv("amazon_watches.csv", index=False)

print("Data successfully extracted and CSV saved.")
