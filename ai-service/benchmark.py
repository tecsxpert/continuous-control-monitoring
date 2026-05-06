import requests
import time
import statistics

BASE_URL = "http://127.0.0.1:5000"

# endpoints to test
endpoints = [
    {
        "name": "categorise",
        "url": "/categorise",
        "payload": {"text": "System latency issue detected"}
    },
    {
        "name": "query",
        "url": "/query",
        "payload": {"question": "How to improve performance?"}
    },
    {
        "name": "generate-report",
        "url": "/generate-report",
        "payload": {"input": "Monthly report"}
    }
]

REQUEST_COUNT = 50


def calculate_percentiles(times):
    times.sort()
    return {
        "p50": times[int(0.50 * len(times))],
        "p95": times[int(0.95 * len(times))],
        "p99": times[int(0.99 * len(times))]
    }


def test_endpoint(endpoint):
    times = []

    print(f"\nTesting {endpoint['name']}...")

    for i in range(REQUEST_COUNT):
        start = time.time()

        response = requests.post(
            BASE_URL + endpoint["url"],
            json=endpoint["payload"]
        )

        end = time.time()

        duration = (end - start) * 1000  # ms
        times.append(duration)

        print(f"Request {i+1}: {round(duration,2)} ms")

    stats = calculate_percentiles(times)

    print(f"\nResults for {endpoint['name']}:")
    print(f"p50: {round(stats['p50'],2)} ms")
    print(f"p95: {round(stats['p95'],2)} ms")
    print(f"p99: {round(stats['p99'],2)} ms")

    return stats


def run_benchmark():
    results = {}

    for ep in endpoints:
        results[ep["name"]] = test_endpoint(ep)

    return results


if __name__ == "__main__":
    run_benchmark()