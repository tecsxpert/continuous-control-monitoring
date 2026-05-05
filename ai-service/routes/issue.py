from flask import Blueprint, request, jsonify, current_app
from services.issue_service import create_issue, generate_report_for_issue
from services.storage import issues

issue_bp = Blueprint("issue", __name__)

@issue_bp.route("/", methods=["POST"])
def create():
    data = request.json

    if not data or not data.get("title") or not data.get("description"):
        return jsonify({"error": "Invalid input"}), 400

    issue = create_issue(data["title"], data["description"])

    executor = current_app.extensions.get("executor")

    if executor:
        executor.submit(generate_report_for_issue, issue)
    else:
        print("Executor not found")
    return jsonify({
        "message": "Issue created",
        "issue_id": issue["id"],
        "status": "processing"
    })


@issue_bp.route("/<issue_id>", methods=["GET"])
def get_issue(issue_id):
    issue = issues.get(issue_id)

    if not issue:
        return jsonify({"error": "Not found"}), 404

    return jsonify(issue)