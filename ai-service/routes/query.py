from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from services.chroma_client import ChromaClient

query_bp = Blueprint("query", __name__)

groq = GroqClient()
chroma = ChromaClient()

@query_bp.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Please provide 'question'"}), 400

        question = data["question"].strip()

        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400

        # Search top 3 similar docs
        sources = chroma.collection.query(
            query_texts=[question],
            n_results=3
        )["documents"][0]

        context = "\n".join(sources)

        prompt = f"""
You are a professional AI assistant.

Use ONLY the provided context.
If context is insufficient, clearly say so.

Answer in concise bullet points or short paragraphs.

Context:
{context}

Question:
{question}
"""

        answer = groq.generate_text(prompt)

        return jsonify({
            "answer": answer,
            "sources": sources
        })

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500