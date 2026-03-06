# Setup and Run

This guide assumes Grafana, Prometheus, and Alertmanager are already installed on Linux.

## 1. Run the custom exporter

```bash
cd grafana-alerts/exporter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python custom_exporter.py
```

Exporter endpoints:
- `GET /metrics` on port `9108`
- `POST /set?value=80`
- `POST /spike?delta=70`
- `POST /threshold?value=40`
- `POST /mode?name=chaos`
- `POST /mode?name=manual`

## 2. Run the webhook receiver

Open another terminal:

```bash
cd grafana-alerts/webhook
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python alert_webhook.py
```

Webhook endpoints:
- `POST /alertmanager`
- `POST /grafana`
- `GET /health`

Logs are written to `grafana-alerts/webhook/alerts.log`.

## 3. Quick health checks

```bash
curl -s http://localhost:9108/health | jq .
curl -s http://localhost:5001/health | jq .
curl -s http://localhost:9108/metrics | grep custom_signal
```

If jq is unavailable, remove `| jq .`.
