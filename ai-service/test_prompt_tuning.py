import requests

BASE_URL = "http://127.0.0.1:5000"

categorise_tests = [
    "Unauthorized login detected in admin panel",
    "Server is slow during traffic",
    "Finance report pending approval",
    "Employee harassment complaint filed",
    "Backup system failed overnight",
    "Audit policy needs review",
    "Password leaked publicly",
    "Website response delayed",
    "Payroll issue in HR",
    "General team meeting tomorrow"
]

query_tests = [
    "How to prevent unauthorized login?",
    "How to improve slow server speed?",
    "What should finance review monthly?",
    "Why are backups important?",
    "How to improve compliance training?",
    "How to secure admin panel?",
    "What helps system performance?",
    "How to protect passwords?",
    "How to handle HR complaints?",
    "What is general operations guidance?"
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