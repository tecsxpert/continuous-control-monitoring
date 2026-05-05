from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from services.cache_instance import cache
import json
import re

categorise_bp = Blueprint("categorise", __name__)

client = GroqClient()


@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Please provide 'text' in JSON body"}), 400

        user_text = data["text"].strip()

        if not user_text:
            return jsonify({"error": "Text cannot be empty"}), 400


        cached = cache.get(user_text)

        if cached:
            cached["meta"] = {
                "is_fallback": False
            }
            return jsonify(cached)


        prompt = f"""
You are an expert text classification AI.

Choose EXACTLY ONE category from:

Security = passwords, hacking, unauthorized access, leaks, threats
Performance = slow systems, delays, speed, latency, downtime
Compliance = audits, regulations, policy adherence, legal review
Operations = backups, maintenance, deployments, daily processes
Finance = payroll, salary, budget, invoices, finance reports
HR = employees, harassment, complaints, hiring, leave, team matters
General = meetings, announcements, uncategorized topics

Return ONLY valid JSON:
{{
  "category": "CategoryName",
  "confidence": 0.0,
  "reasoning": "Short reason"
}}

Text:
{user_text}
"""


        ai_response = client.generate_text(prompt)

        if ai_response["success"]:
            response_text = ai_response["text"]
            is_fallback = False
        else:
            return jsonify({
                "category": "General",
                "confidence": 0.3,
                "reasoning": "Fallback due to AI error",
                "meta": {
                    "is_fallback": True
                }
            })


        match = re.search(r'\{.*\}', response_text, re.DOTALL)

        if not match:
            return jsonify({
                "category": "General",
                "confidence": 0.50,
                "reasoning": "Could not parse AI response",
                "meta": {
                    "is_fallback": True
                }
            })


        result = json.loads(match.group())


        result["meta"] = {
            "is_fallback": False
        }


        cache.set(user_text, result)


        return jsonify(result)

    except Exception as error:
        return jsonify({
            "category": "General",
            "confidence": 0.0,
            "reasoning": str(error),
            "meta": {
                "is_fallback": True
            }
        }), 500