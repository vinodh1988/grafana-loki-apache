import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

import requests

BASE_URL = os.getenv("TARGET_BASE_URL", "http://web").rstrip("/")
MIN_RPS = int(os.getenv("MIN_RPS", "3"))
MAX_RPS = int(os.getenv("MAX_RPS", "30"))
WINDOW_SECONDS = int(os.getenv("WINDOW_SECONDS", "6"))
WORKERS = int(os.getenv("WORKERS", "20"))
TIMEOUT = float(os.getenv("REQ_TIMEOUT_SECONDS", "4.0"))

WEIGHTED_PATHS = [
    ("/", 18),
    ("/health.php", 12),
    ("/api/users.php", 16),
    ("/api/orders.php", 14),
    ("/api/payments.php", 12),
    ("/api/inventory.php", 12),
    ("/api/unstable.php", 10),
    ("/api/not-found-simulator.php", 4),
    ("/api/unknown-" + str(random.randint(1, 9999)) + ".php", 2),
]

session = requests.Session()


def pick_path() -> str:
    paths, weights = zip(*WEIGHTED_PATHS)
    return random.choices(paths, weights=weights, k=1)[0]


def hit_endpoint() -> int:
    path = pick_path()
    url = f"{BASE_URL}{path}"
    headers = {
        "User-Agent": random.choice([
            "loadgen-bot/1.0",
            "synthetic-client/2.1",
            "chaos-checker/0.9",
        ])
    }
    try:
        response = session.get(url, timeout=TIMEOUT, headers=headers)
        return response.status_code
    except requests.RequestException:
        return 0


def run_window() -> None:
    target_rps = random.randint(MIN_RPS, MAX_RPS)
    request_count = target_rps * WINDOW_SECONDS
    start = time.time()

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        status_codes = list(pool.map(lambda _: hit_endpoint(), range(request_count)))

    elapsed = max(time.time() - start, 0.001)
    effective_rps = round(request_count / elapsed, 2)

    summary = {}
    for code in status_codes:
        summary[code] = summary.get(code, 0) + 1

    print(
        f"window={WINDOW_SECONDS}s target_rps={target_rps} effective_rps={effective_rps} statuses={summary}",
        flush=True,
    )


def main() -> None:
    print(
        f"Starting loadgen against {BASE_URL} with random RPS between {MIN_RPS} and {MAX_RPS}",
        flush=True,
    )
    while True:
        run_window()
        time.sleep(random.uniform(0.4, 1.7))


if __name__ == "__main__":
    main()
