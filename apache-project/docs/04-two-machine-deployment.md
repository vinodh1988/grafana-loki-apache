# Two-Machine Deployment (Your Setup)

This guide matches your architecture:

- Machine A: Apache app + Apache exporter + Loki + Promtail + load generator (Docker Compose)
- Machine B: Prometheus + Grafana as Linux services (already installed)

## 1. Deploy Machine A (Apache/Loki host)

From project root on Machine A:

```bash
docker compose up -d --build
```

Exposed ports on Machine A:

- Apache app: `8088`
- Apache exporter metrics: `9117`
- Loki API: `3100`

Open firewall from Machine B to Machine A:

- TCP `9117` for Prometheus scraping
- TCP `3100` for Grafana Loki datasource

## 2. Configure Prometheus on Machine B

Edit `/etc/prometheus/prometheus.yml` and add the job snippet from:

- `monitoring/prometheus/apache-remote-job.yml`

Use Machine A IP/FQDN in place of `<APACHE_LOKI_HOST>`.

Example:

```yaml
- job_name: apache_remote
  scrape_interval: 5s
  static_configs:
    - targets: ["10.50.20.41:9117"]
      labels:
        site: apache-loki-remote
```

Validate and restart Prometheus:

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
sudo systemctl restart prometheus
sudo systemctl status prometheus --no-pager
```

Then verify in Prometheus UI on Machine B:

- `Status -> Targets`
- `job="apache_remote"` should be `UP`

## 3. Configure Grafana on Machine B

Create/update data sources in Grafana:

- Prometheus URL: `http://localhost:9090`
- Loki URL: `http://<APACHE_LOKI_HOST>:3100`

Keep datasource UIDs exactly:

- Prometheus uid: `prometheus`
- Loki uid: `loki`

These UIDs are used by dashboard JSON panels.

## 4. Import dashboard in Grafana

Import file:

- `monitoring/grafana/dashboards/apache-observability-dashboard.json`

After import, the dashboard shows:

- Apache availability/workers/CPU/load metrics from Prometheus
- Status-code and latency insights from Loki logs
- Error/warn stream from Apache error logs

## 5. Verify end-to-end quickly

On Machine B Prometheus UI:

- `up{job="apache_remote"}`
- `apache_accesses_total`
- `apache_workers{state="busy"}`

On Machine B Grafana Explore with Loki datasource:

- `{job="apache_access"}`
- `{job="apache_error"}`

## 6. Common issues

- `Target DOWN` in Prometheus: check firewall and Machine A `9117` reachability.
- Grafana Loki datasource error: check Machine B can reach Machine A `3100`.
- No logs: verify `promtail` container is running and reading `/var/log/apache2` volume.
