# grafana-alerts

A complete alert handling demo where both Prometheus Alertmanager and Grafana Alerting send alerts to your own Python webhook, using a custom metric exporter with controllable spikes and dynamic thresholds.

## Project Structure

- `exporter/custom_exporter.py`: custom Prometheus exporter with artificial spike endpoints.
- `webhook/alert_webhook.py`: Python webhook that accepts Alertmanager and Grafana alerts.
- `prometheus/alerts.yml`: alert rules for warning and critical thresholds.
- `prometheus/prometheus-snippet.yml`: scrape and rule loading snippet for Prometheus.
- `prometheus/alertmanager-snippet.yml`: webhook receiver and routing snippet for Alertmanager.
- `scripts/demo-spikes.sh`: Linux script to trigger alert scenarios.
- `docs/01-setup-and-run.md`: install and run instructions.
- `docs/02-prometheus-alertmanager.md`: Prometheus + Alertmanager integration details.
- `docs/03-grafana-alerting-ui-guide.md`: Grafana UI-only alert setup guide.
- `docs/04-test-scenarios.md`: end-to-end test scenarios.

## Docs Order

1. Start with `docs/01-setup-and-run.md`
2. Continue with `docs/02-prometheus-alertmanager.md`
3. Then `docs/03-grafana-alerting-ui-guide.md`
4. Run checks in `docs/04-test-scenarios.md`
