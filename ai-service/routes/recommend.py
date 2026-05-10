from flask import Blueprint, request, jsonify
from datetime import datetime
from services.groq_client import generate_response
import json

recommend_bp = Blueprint('recommend', __name__)


def load_prompt():
    with open("prompts/recommend_prompt.txt", "r") as f:
        return f.read()


@recommend_bp.route('/', methods=['POST'])
def recommend():
    data = request.json

    if not data or "title" not in data or "description" not in data:
        return jsonify({
            "error": "title and description are required"
        }), 400

    title = data["title"]
    description = data["description"]

    prompt_template = load_prompt()
    final_prompt = prompt_template.format(
        title=title,
        description=description
    )

    ai_output = generate_response(final_prompt)

    print("RAW AI OUTPUT:", ai_output)

    if not ai_output:
        return jsonify({
            "error": "AI service unavailable"
        }), 500

    try:
        recommendations = json.loads(ai_output)
    except Exception:
        return jsonify({
            "status": "failed",
            "error": "Invalid AI response"
        }), 500

        if not isinstance(recommendations, list) or len(recommendations) != 3:
            raise ValueError("AI did not return exactly 3 recommendations")

        for item in recommendations:
            if "action_type" not in item:
                item["action_type"] = item.get("type", "unknown")

            if "description" not in item:
                raise ValueError("Missing description")

            if "priority" not in item:
                raise ValueError("Missing priority")

            if item["priority"] not in ["high", "medium", "low"]:
                item["priority"] = "medium"  

    except Exception as e:
        return jsonify({
            "error": "Invalid AI response format",
            "details": str(e),
            "raw_output": ai_output
        }), 500

    return jsonify({
        "recommendations": recommendations,
        "generated_at": datetime.utcnow().isoformat()
    })