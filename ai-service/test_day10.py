import requests

BASE_URL = "http://127.0.0.1:5000"

categorise_tests = [
    "User password leaked online",
    "System latency increased during peak hours",
    "Annual compliance audit required",
    "Daily backup failed due to error",
    "Budget planning for next quarter",
    "Employee resignation notice",
    "Database response is slow",
    "Security breach detected",
    "Payroll delay issue",
    "Team meeting scheduled tomorrow"
]

query_tests = [
    "How to prevent password leaks?",
    "How to improve database performance?",
    "What is compliance audit?",
    "How to fix backup failures?",
    "How to manage budget planning?",
    "How to handle employee resignation?",
    "How to reduce latency?",
    "How to detect security breaches?",
    "How to fix payroll delays?",
    "What are general meeting guidelines?"
]


print("\n===== TESTING /categorise =====\n")

for text in categorise_tests:
    response = requests.post(
        f"{BASE_URL}/categorise",
        json={"text": text}
    )
    print("INPUT :", text)
    print("OUTPUT:", response.json())
    print("-" * 50)


print("\n===== TESTING /query =====\n")

for question in query_tests:
    response = requests.post(
        f"{BASE_URL}/query",
        json={"question": question}
    )
    print("QUESTION:", question)
    print("OUTPUT:", response.json())
    print("-" * 50)