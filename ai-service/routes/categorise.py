from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
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
  "confidence": 0.00,
  "reasoning": "Short reason"
}}

Text:
{user_text}
"""

        response = client.generate_text(prompt)

        match = re.search(r'\{.*\}', response, re.DOTALL)

        if not match:
            return jsonify({
                "category": "General",
                "confidence": 0.50,
                "reasoning": "Could not parse AI response"
            })

        result = json.loads(match.group())

        return jsonify(result)

    except Exception as error:
        return jsonify({
            "category": "General",
            "confidence": 0.0,
            "reasoning": str(error)
        }), 500