import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

        self.response_times = []

    def generate_text(self, prompt):
        start = time.time()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300
            )

            result = response.choices[0].message.content.strip()

            elapsed = (time.time() - start) * 1000
            self.response_times.append(elapsed)

            self.response_times = self.response_times[-10:]

            return result

        except Exception as e:
            return "Error: " + str(e)

    def get_avg_response_time(self):
        if not self.response_times:
            return 0
        return sum(self.response_times) / len(self.response_times)