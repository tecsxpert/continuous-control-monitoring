from flask import Blueprint, request, jsonify
from services.job_manager import job_manager
import threading
import time
import requests

report_bp = Blueprint("report", __name__)


def generate_report(job_id, data):
    time.sleep(5)

    result = f"Report generated for input: {data}"

    job_manager.update_job(job_id, result)

    try:
        requests.post(
            "http://example.com/webhook",
            json={
                "job_id": job_id,
                "result": result
            }
        )
    except:
        pass


@report_bp.route("/generate-report", methods=["POST"])
def generate_report_api():
    data = request.get_json()

    if not data or "input" not in data:
        return jsonify({"error": "Provide 'input'"}), 400

    job_id = job_manager.create_job()

    thread = threading.Thread(
        target=generate_report,
        args=(job_id, data["input"])
    )
    thread.start()

    return jsonify({
        "message": "Report generation started",
        "job_id": job_id
    })

@report_bp.route("/job-status/<job_id>", methods=["GET"])
def job_status(job_id):
    job = job_manager.get_job(job_id)

    if not job:
        return jsonify({"error": "Invalid job_id"}), 404

    return jsonify(job)