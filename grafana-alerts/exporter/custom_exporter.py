import random
import threading
import time
from dataclasses import dataclass, asdict

from flask import Flask, Response, jsonify, request
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)

registry = CollectorRegistry()
signal_gauge = Gauge(
    "custom_signal_value",
    "Artificial signal value for alert testing.",
    registry=registry,
)
threshold_gauge = Gauge(
    "custom_threshold_value",
    "Dynamic threshold used by alerts.",
    registry=registry,
)
over_threshold_gauge = Gauge(
    "custom_signal_over_threshold",
    "1 when signal is above threshold, else 0.",
    registry=registry,
)


@dataclass
class ExporterState:
    signal: float = 30.0
    threshold: float = 60.0
    mode: str = "manual"


state = ExporterState()
state_lock = threading.Lock()
stop_event = threading.Event()


def publish_metrics() -> None:
    with state_lock:
        signal = state.signal
        threshold = state.threshold

    signal_gauge.set(signal)
    threshold_gauge.set(threshold)
    over_threshold_gauge.set(1.0 if signal > threshold else 0.0)


def chaos_loop() -> None:
    while not stop_event.is_set():
        with state_lock:
            if state.mode != "chaos":
                time.sleep(0.2)
                continue

            # Drastic and irregular changes to trigger alert transitions quickly.
            drift = random.uniform(-20.0, 20.0)
            surge = random.choice([0.0, 0.0, 35.0, -30.0, 50.0])
            threshold_shift = random.uniform(-18.0, 12.0)

            state.signal = max(0.0, state.signal + drift + surge)
            state.threshold = max(5.0, state.threshold + threshold_shift)

        publish_metrics()
        time.sleep(1.0)


@app.route("/metrics")
def metrics() -> Response:
    publish_metrics()
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)


@app.route("/health")
def health() -> Response:
    return jsonify({"status": "ok", "state": asdict(state)})


@app.route("/state")
def get_state() -> Response:
    with state_lock:
        return jsonify(asdict(state))


@app.route("/set", methods=["POST"])
def set_signal() -> Response:
    value = request.args.get("value", type=float)
    if value is None:
        return jsonify({"error": "Missing query param: value"}), 400

    with state_lock:
        state.signal = max(0.0, value)
    publish_metrics()
    return jsonify({"message": "signal updated", "state": asdict(state)})


@app.route("/spike", methods=["POST"])
def spike_signal() -> Response:
    delta = request.args.get("delta", default=50.0, type=float)
    with state_lock:
        state.signal = max(0.0, state.signal + delta)
    publish_metrics()
    return jsonify({"message": "signal spiked", "state": asdict(state)})


@app.route("/threshold", methods=["POST"])
def set_threshold() -> Response:
    value = request.args.get("value", type=float)
    if value is None:
        return jsonify({"error": "Missing query param: value"}), 400

    with state_lock:
        state.threshold = max(1.0, value)
    publish_metrics()
    return jsonify({"message": "threshold updated", "state": asdict(state)})


@app.route("/mode", methods=["POST"])
def set_mode() -> Response:
    name = request.args.get("name", default="manual", type=str)
    if name not in {"manual", "chaos"}:
        return jsonify({"error": "mode must be one of: manual, chaos"}), 400

    with state_lock:
        state.mode = name
    return jsonify({"message": "mode updated", "state": asdict(state)})


if __name__ == "__main__":
    publish_metrics()

    worker = threading.Thread(target=chaos_loop, daemon=True)
    worker.start()

    app.run(host="0.0.0.0", port=9108)
