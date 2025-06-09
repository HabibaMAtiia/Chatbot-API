import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI-compatible client (Groq)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=OPENAI_API_KEY
)

# Define system prompt for grocery sorting
system_prompt = "You are a helpful grocery assistant that organizes shopping items into clear categories."

# Function to process and categorize shopping items
def categorize_items(user_input: str) -> str:
    try:
        prompt = f"""
You are an assistant that categorizes and sorts grocery items.

Here is a list of grocery items:

{user_input}

Please:

1. Categorize these items using specific categories like Vegetables, Fruits, Dairy, Meat, Bakery, Beverages, etc.
2. Avoid broad terms like 'Produce' — use 'Vegetables' and 'Fruits' instead.
3. Sort items alphabetically within each category.
4. Present the list in a clean, bullet-point format.
"""

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            top_p=0.9,
            max_tokens=512
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
