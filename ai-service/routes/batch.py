from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
import time
import json

batch_bp = Blueprint("batch", __name__)


@batch_bp.route("/", methods=["POST"])
def batch_process():
    data = request.json

    if not data or "items" not in data:
        return jsonify({"error": "Missing items"}), 400

    items = data["items"]

    if len(items) > 20:
        return jsonify({"error": "Maximum 20 items allowed"}), 400

    results = []

    for item in items:
        title = item.get("title")
        description = item.get("description")

        if not title or not description:
            results.append({
                "status": "failed",
                "error": "Invalid input"
            })
            continue

        try:
            prompt = f"""
You are a cybersecurity auditor.

Analyze the issue and generate a clear, concise risk description.

Title: {title}
Description: {description}

Instructions:
- Do NOT include headings or labels
- Do NOT use markdown or formatting symbols
- Return ONLY plain text
- Keep it professional and concise (2–3 lines)
"""

            ai_output = generate_response(prompt)

            results.append({
                "status": "success",
                "result": ai_output
            })

        except Exception as e:
            results.append({
                "status": "failed",
                "error": str(e)
            })

        time.sleep(0.1)

    return jsonify({
        "results": results
    })