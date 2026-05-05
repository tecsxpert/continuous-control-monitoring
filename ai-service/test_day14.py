import requests

BASE_URL = "http://127.0.0.1:5000"

test_cases = [
    # Security
    {"type": "categorise", "input": "User password leaked online"},
    {"type": "query", "input": "How to prevent password leaks?"},

    # Performance
    {"type": "categorise", "input": "System latency increased"},
    {"type": "query", "input": "How to improve system performance?"},

    # Compliance
    {"type": "categorise", "input": "Annual compliance audit required"},
    {"type": "query", "input": "What is a compliance audit?"},

    # Operations
    {"type": "categorise", "input": "Daily backup failed"},
    {"type": "query", "input": "How to fix backup failures?"},

    # Finance
    {"type": "categorise", "input": "Payroll delay issue"},
    {"type": "query", "input": "How to manage payroll delays?"},

    # HR
    {"type": "categorise", "input": "Employee resignation notice"},
    {"type": "query", "input": "How to handle employee resignation?"},

    # General
    {"type": "categorise", "input": "Team meeting scheduled"},
    {"type": "query", "input": "How to conduct effective meetings?"},

    # Extra mixed cases
    {"type": "categorise", "input": "Unauthorized access detected"},
    {"type": "query", "input": "How to detect security breaches?"},

    {"type": "categorise", "input": "Database is slow"},
    {"type": "query", "input": "How to optimize database performance?"},

    {"type": "categorise", "input": "Budget planning discussion"},
    {"type": "query", "input": "How to plan a budget effectively?"},

    {"type": "categorise", "input": "Server downtime occurred"},
    {"type": "query", "input": "How to prevent downtime?"},

    {"type": "categorise", "input": "Employee complaint filed"},
    {"type": "query", "input": "How to handle employee complaints?"},

    {"type": "categorise", "input": "Invoice processing delay"},
    {"type": "query", "input": "How to manage invoices?"},

    {"type": "categorise", "input": "Backup completed successfully"},
    {"type": "query", "input": "Best practices for backups?"},

    {"type": "categorise", "input": "System running slow"},
    {"type": "query", "input": "Ways to reduce latency?"}
]


print("\n===== DAY 14 PROMPT QA TEST =====\n")

for i, case in enumerate(test_cases, 1):
    try:
        if case["type"] == "categorise":
            response = requests.post(
                f"{BASE_URL}/categorise",
                json={"text": case["input"]}
            )
        else:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"question": case["input"]}
            )

        print(f"\nTest {i}")
        print("INPUT :", case["input"])
        print("OUTPUT:", response.json())

    except Exception as e:
        print(f"Error in test {i}: {e}")