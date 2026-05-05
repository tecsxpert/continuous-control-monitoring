from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import generate_response
from services.rag_service import retrieve
import json

report_bp = Blueprint('report', __name__)


def load_prompt():
    with open("prompts/report_prompt.txt", "r") as f:
        return f.read()


@report_bp.route('/', methods=['POST'])
def generate_report():
    data = request.json

    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "title and description are required"}), 400

    title = data["title"]
    description = data["description"]

    query = title + " " + description
    context_chunks = retrieve(query)
    context = "\n".join(context_chunks)

    prompt_template = load_prompt()
    final_prompt = prompt_template.format(
        title=title,
        description=description,
        context=context
    )

    ai_output = generate_response(final_prompt)

    print("RAW REPORT OUTPUT:", ai_output)

    if not ai_output:
        return jsonify({"error": "AI service unavailable"}), 500

    try:
        report = json.loads(ai_output)
    except Exception:
        return jsonify({
            "error": "Invalid AI response",
            "raw_output": ai_output
        }), 500

    return jsonify({
        "report": report,
        "generated_at": datetime.utcnow().isoformat()
    })