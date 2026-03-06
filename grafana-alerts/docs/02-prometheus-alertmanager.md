# Prometheus and Alertmanager Setup

## 1. Add alert rules to Prometheus host

Copy `grafana-alerts/prometheus/alerts.yml` to your Prometheus server:

```bash
sudo cp grafana-alerts/prometheus/alerts.yml /etc/prometheus/alerts.yml
```

## 2. Update Prometheus config

Use `grafana-alerts/prometheus/prometheus-snippet.yml` as reference and ensure your `/etc/prometheus/prometheus.yml` includes:

- `rule_files: ["/etc/prometheus/alerts.yml"]`
- scrape target `job_name: grafana_alerts_exporter`
- exporter target `<EXPORTER_HOST>:9108`

Example target when exporter runs on same machine as Prometheus:

```yaml
- job_name: grafana_alerts_exporter
  scrape_interval: 5s
  static_configs:
    - targets: ["localhost:9108"]
```

Reload/restart Prometheus.

## 3. Configure Alertmanager webhook receiver

Use `grafana-alerts/prometheus/alertmanager-snippet.yml` as reference and update `/etc/alertmanager/alertmanager.yml`:

- Set receiver webhook URL to `http://<WEBHOOK_HOST>:5001/alertmanager`
- Keep routes for `severity=warning` and `severity=critical`

Example if webhook runs on same host as Alertmanager:

```yaml
webhook_configs:
  - url: http://localhost:5001/alertmanager
```

Reload/restart Alertmanager.

## 4. Validate Prometheus side

Check target status in Prometheus UI:
- `Status -> Targets`
- `grafana_alerts_exporter` must be `UP`

Check rules in Prometheus UI:
- `Alerts`
- Confirm both alerts are listed and move `inactive -> pending -> firing` during spikes.
