import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_recipe(ingredients_text: str, category: str, cuisine: str = "Any", health: str = "None") -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "http://localhost:8501/Smart_Recipe_Generator",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a professional AI chef.

Generate a {category.lower()} recipe using ONLY these ingredients:
{ingredients_text.strip()}

Cuisine: {cuisine}
Health Preference: {health}

You may use pantry items like oil, salt, water, and common spices.

Respond in this format:
- Title
- Ingredients
- Steps
- Estimated Cooking Time
"""

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a professional chef AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 700,
        "top_p": 0.9
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"❌ API Error: {result.get('error', {}).get('message', 'No response')}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"
