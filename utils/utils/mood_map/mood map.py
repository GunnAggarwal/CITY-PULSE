# Mood map logic will go here
import requests
import os
from textblob import TextBlob 

NEWS_API_KEY = os.getenv("NEWS_API_KEY") 

def get_city_mood(city):
    url = "https://newsapi.org/v2/everything"
    query = f"{city} AND news"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 15
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        mood_score = 0
        mood_details = {"Positive": 0, "Neutral": 0, "Negative": 0}
        headlines = []

        for article in articles:
            title = article.get("title", "")
            blob = TextBlob(title)
            polarity = blob.sentiment.polarity
            headlines.append(title)

            if polarity > 0.1:
                mood_details["Positive"] += 1
            elif polarity < -0.1:
                mood_details["Negative"] += 1
            else:
                mood_details["Neutral"] += 1

        # Determine overall mood
        if mood_details["Positive"] > mood_details["Negative"]:
            mood = "Happy 😊"
        elif mood_details["Negative"] > mood_details["Positive"]:
            mood = "Sad 😔"
        else:
            mood = "Neutral 😐"

        return {
            "mood": mood,
            "details": mood_details,
            "headlines": headlines
        }

    except Exception as e:
        return {"error": str(e)}
