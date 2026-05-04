from flask import Blueprint, jsonify
import time
from services.groq_client import GroqClient
from services.chroma_client import ChromaClient
from services.redis_cache import RedisCache
from services.cache_instance import cache

health_bp = Blueprint("health", __name__)

groq = GroqClient()
chroma = ChromaClient()

start_time = time.time()

@health_bp.route("/health", methods=["GET"])
def health():
    uptime = time.time() - start_time

    return jsonify({
        "status": "ok",
        "model": groq.model,
        "avg_response_time_ms": round(groq.get_avg_response_time(), 2),
        "uptime_seconds": round(uptime, 2),
        "documents_in_db": chroma.get_document_count(),
        "cache": cache.stats()
    })