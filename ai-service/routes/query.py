from flask import Blueprint, request, jsonify
import time
from services.groq_client import GroqClient
from services.chroma_client import ChromaClient
from services.redis_cache import RedisCache
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

        cached = None

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
                    "cached": True
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


        response = groq.client.chat.completions.create(
            model=groq.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )

        answer = response.choices[0].message.content.strip()


        tokens_used = len(prompt.split()) + len(answer.split())


        cache.set(question, {
            "answer": answer,
            "sources": sources
        })


        response_time = (time.time() - start_time) * 1000


        return jsonify({
            "answer": answer,
            "sources": sources,
            "meta": {
                "confidence": 0.85,
                "model_used": groq.model,
                "tokens_used": tokens_used,
                "response_time_ms": round(response_time, 2),
                "cached": False
            }
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500