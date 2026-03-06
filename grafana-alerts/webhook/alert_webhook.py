import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request


app = Flask(__name__)
log_file = Path(__file__).resolve().parent / "alerts.log"


def append_log(record: dict) -> None:
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True) + "\n")


def normalize_alertmanager(payload: dict) -> dict:
    return {
        "source": "alertmanager",
        "received_at": datetime.now(timezone.utc).isoformat(),
        "status": payload.get("status"),
        "receiver": payload.get("receiver"),
        "groupLabels": payload.get("groupLabels", {}),
        "commonLabels": payload.get("commonLabels", {}),
        "commonAnnotations": payload.get("commonAnnotations", {}),
        "alerts": payload.get("alerts", []),
        "externalURL": payload.get("externalURL"),
    }


def normalize_grafana(payload: dict) -> dict:
    return {
        "source": "grafana",
        "received_at": datetime.now(timezone.utc).isoformat(),
        "title": payload.get("title"),
        "state": payload.get("state") or payload.get("status"),
        "message": payload.get("message"),
        "ruleName": payload.get("ruleName"),
        "orgId": payload.get("orgId"),
        "alerts": payload.get("alerts", []),
        "raw": payload,
    }


@app.route("/health")
def health():
    return jsonify({"status": "ok", "log_file": str(log_file)})


@app.route("/alertmanager", methods=["POST"])
def alertmanager_webhook():
    payload = request.get_json(silent=True) or {}
    record = normalize_alertmanager(payload)
    append_log(record)

    print("[ALERTMANAGER]", json.dumps(record, ensure_ascii=True))
    return jsonify({"status": "accepted", "source": "alertmanager"}), 200


@app.route("/grafana", methods=["POST"])
def grafana_webhook():
    payload = request.get_json(silent=True) or {}
    record = normalize_grafana(payload)
    append_log(record)

    print("[GRAFANA]", json.dumps(record, ensure_ascii=True))
    return jsonify({"status": "accepted", "source": "grafana"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
