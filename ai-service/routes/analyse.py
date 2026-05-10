from flask import Blueprint, request, jsonify
from services.groq_client import generate_response
import json

analyse_bp = Blueprint("analyse", __name__)

@analyse_bp.route("/", methods=["POST"])
def analyse_document():
    data = request.json

    if not data or not data.get("text"):
        return jsonify({"error": "Missing text"}), 400

    text = data["text"]

    try:
        with open("prompts/analyse_prompt.txt") as f:
            prompt_template = f.read()

        final_prompt = prompt_template.format(text=text)

        ai_output = generate_response(final_prompt)

        findings = json.loads(ai_output)

        return jsonify({
            "findings": findings
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "AI analysis failed"}), 500