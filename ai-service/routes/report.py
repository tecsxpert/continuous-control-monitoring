from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from services.groq_client import generate_response
from services.rag_service import retrieve
from services.cache import redis_client
from services.groq_client import stream_response
import json
import hashlib

report_bp = Blueprint('report', __name__)
@report_bp.route("/stream", methods=["GET"])

def stream_report():
    title = request.args.get("title")
    description = request.args.get("description")

    if not title or not description:
        return {"error": "Missing input"}, 400

    def generate():
        yield "data: started\n\n"

        buffer = ""
        for chunk in stream_response(title, description):
            buffer += chunk
            if "." in buffer or "\n" in buffer:
                yield f"data: {buffer.strip()}\n\n"
                buffer = ""
                yield f"data: {buffer}\n\n"
                buffer = ""

        if buffer:
            yield f"data: {buffer}\n\n"

        yield "event: done\ndata: end\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        },
    )

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

    cache_key = get_cache_key(title, description)

    try:
        cached = redis_client.get(cache_key)
    except:
        cached = None
    if cached:
        return jsonify({
            "status": "success",
            "data": report,
            "cached": False
        })

    query = title + " " + description
    context_chunks = retrieve(query)
    context = "\n".join(context_chunks)

    prompt_template = load_prompt()
    final_prompt = prompt_template.format(
        context=context,
        title=title,
        description=description
    )

    ai_output = generate_response(final_prompt)

    print("RAW REPORT OUTPUT:", ai_output)

    if not ai_output:
        return jsonify({"error": "AI service unavailable"}), 500

    try:
        def clean_json_output(output):
            output = output.replace("```json", "").replace("```", "")
            start = output.find("{")
            end = output.rfind("}") + 1
            return output[start:end]


        cleaned_output = clean_json_output(ai_output)

        try:
            report = json.loads(cleaned_output)
        except Exception as e:
            return jsonify({
                "error": "Invalid AI response",
                "raw_output": ai_output
            }), 500
        try:
            redis_client.setex(cache_key, 600, json.dumps(report))
        except:
            pass
    except Exception:
        return jsonify({
            "error": "Invalid AI response",
            "raw_output": ai_output
        }), 500

    return jsonify({
        "report": report,
        "generated_at": datetime.utcnow().isoformat()
    })

def get_cache_key(title, description):
    return hashlib.md5(f"{title}:{description}".encode()).hexdigest()