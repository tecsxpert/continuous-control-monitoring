from services.storage import issues
from services.groq_client import generate_response
from services.rag_service import retrieve
import json
import uuid

def create_issue(title, description):
    issue_id = str(uuid.uuid4())

    issue = {
        "id": issue_id,
        "title": title,
        "description": description,
        "ai_report": None
    }

    issues[issue_id] = issue

    return issue


def attach_ai_report(issue_id, report):
    if issue_id in issues:
        issues[issue_id]["ai_report"] = report


def generate_report_for_issue(issue):
    try:
        query = issue["title"] + " " + issue["description"]
        context = "\n".join(retrieve(query))

        with open("prompts/report_prompt.txt") as f:
            prompt = f.read()

        final_prompt = prompt.format(
            title=issue["title"],
            description=issue["description"],
            context=context
        )

        ai_output = generate_response(final_prompt)

        if ai_output:
            report = json.loads(ai_output)
            attach_ai_report(issue["id"], report)

    except Exception as e:
        print("AI failed:", e)