import requests
import time

BASE_URL = "http://127.0.0.1:5000"

print("\n===== DAY 16 FINAL VERIFICATION =====\n")


print("Testing /categorise...\n")

start = time.time()

response1 = requests.post(
    f"{BASE_URL}/categorise",
    json={"text": "Server latency issue"}
)

time1 = (time.time() - start) * 1000

print("First Response:")
print(response1.json())
print(f"Response Time: {round(time1,2)} ms\n")


start = time.time()

response2 = requests.post(
    f"{BASE_URL}/categorise",
    json={"text": "Server latency issue"}
)

time2 = (time.time() - start) * 1000

print("Second Response (Cache Expected):")
print(response2.json())
print(f"Response Time: {round(time2,2)} ms\n")



print("Testing /query...\n")

start = time.time()

query1 = requests.post(
    f"{BASE_URL}/query",
    json={"question": "How to improve system performance?"}
)

query_time1 = (time.time() - start) * 1000

print("First Query:")
print(query1.json())
print(f"Response Time: {round(query_time1,2)} ms\n")


start = time.time()

query2 = requests.post(
    f"{BASE_URL}/query",
    json={"question": "How to improve system performance?"}
)

query_time2 = (time.time() - start) * 1000

print("Second Query (Cache Expected):")
print(query2.json())
print(f"Response Time: {round(query_time2,2)} ms\n")


print("Testing /health...\n")

health = requests.get(f"{BASE_URL}/health")

print(health.json())


print("\n===== FINAL VERIFICATION COMPLETE =====")