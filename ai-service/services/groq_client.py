import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Groq Error:", e)
        return None

def stream_response(title, description):
    from groq import Groq
    import os

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
Generate a professional audit report.

Title: {title}
Description: {description}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in completion:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if hasattr(delta, "content") and delta.content:
            yield delta.content