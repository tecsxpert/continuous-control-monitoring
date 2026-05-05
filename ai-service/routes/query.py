from flask import Blueprint, request, jsonify
import time
from services.groq_client import GroqClient
from services.chroma_client import ChromaClient
from services.cache_instance import cache

query_bp = Blueprint("query", __name__)

groq = GroqClient()
chroma = ChromaClient()


@query_bp.route("/query", methods=["POST"])
def query():
    try:
        start_time = time.time()

        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Please provide 'question'"}), 400

        question = data["question"].strip()

        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400


        skip_cache = data.get("skip_cache", False)

        if not skip_cache:
            cached = cache.get(question)

            if cached:
                response_time = (time.time() - start_time) * 1000

                return jsonify({
                    "answer": cached["answer"],
                    "sources": cached["sources"],
                    "meta": {
                        "confidence": 0.95,
                        "model_used": groq.model,
                        "tokens_used": 0,
                        "response_time_ms": round(response_time, 2),
                        "cached": True,
                        "is_fallback": False   # ✅ fixed
                    }
                })


        sources = chroma.collection.query(
            query_texts=[question],
            n_results=3
        )["documents"][0]

        context = "\n".join(sources)


        prompt = f"""
You are a professional AI assistant.

RULES:
- First try to answer using the context
- If context is weak, give a GENERAL helpful answer based on knowledge
- Do NOT just say "insufficient context"
- Always provide useful guidance

Context:
{context}

Question:
{question}
"""


        ai_response = groq.generate_text(prompt)

        if ai_response["success"]:
            answer = ai_response["text"]
            is_fallback = False
        else:
            answer = "Unable to generate response right now. Please try again later."
            is_fallback = True


        tokens_used = len(prompt.split()) + len(answer.split())


        if not is_fallback:
            cache.set(question, {
                "answer": answer,
                "sources": sources
            })


        response_time = (time.time() - start_time) * 1000


        return jsonify({
            "answer": answer,
            "sources": sources,
            "meta": {
                "confidence": 0.85 if not is_fallback else 0.3,
                "model_used": groq.model,
                "tokens_used": tokens_used if not is_fallback else 0,
                "response_time_ms": round(response_time, 2),
                "cached": False,
                "is_fallback": is_fallback   # ✅ FIXED HERE
            }
        })

    except Exception as error:
        return jsonify({
            "error": str(error),
            "meta": {
                "is_fallback": True
            }
        }), 500