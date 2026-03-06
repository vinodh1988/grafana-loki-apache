# apache-project

A complete Apache observability lab that includes:

- Apache website with multiple endpoints and intentional unstable behavior.
- Randomized/fluctuating load generation across endpoints.
- Apache metrics collection via `apache_exporter`.
- Prometheus scrape job for Apache exporter on a remote Prometheus server.
- Loki + Promtail log pipeline for Apache access and error logs.
- Grafana dashboard JSON for metrics + logs on a remote Grafana server.

## Target architecture

- Machine A (this project via Docker): Apache app + apache_exporter + Loki + Promtail + loadgen
- Machine B (already installed as services): Prometheus + Grafana

## Quick start (Machine A)

```bash
docker compose up -d --build
```

Wait around 30-60 seconds for services to become healthy and for loadgen to populate logs/metrics.

Machine A exposed ports:

- Apache app: `http://<MACHINE_A_IP>:8088`
- Apache exporter metrics: `http://<MACHINE_A_IP>:9117/metrics`
- Loki API: `http://<MACHINE_A_IP>:3100`

## Configure Prometheus on Machine B

Use this snippet in `/etc/prometheus/prometheus.yml`:

```yaml
- job_name: apache_remote
  scrape_interval: 5s
  static_configs:
    - targets: ["<MACHINE_A_IP>:9117"]
```

Also available as a file:

- `monitoring/prometheus/apache-remote-job.yml`

Then restart Prometheus service.

## Configure Grafana on Machine B

Create data sources with these URLs:

- Prometheus: `http://localhost:9090`
- Loki: `http://<MACHINE_A_IP>:3100`

Use these datasource UIDs to match dashboard JSON:

- Prometheus uid: `prometheus`
- Loki uid: `loki`

Import dashboard:

- `monitoring/grafana/dashboards/apache-observability-dashboard.json`

## What this project generates

- `2xx`, `4xx`, `5xx` responses from different endpoints.
- Warning/error messages in Apache error logs.
- Variable request rates and latency from fluctuating synthetic load.
- Apache runtime metrics (workers, requests, CPU load, traffic).

## Project layout

- `app/`: Apache website and endpoint code.
- `loadgen/`: synthetic random load generator.
- `monitoring/prometheus/`: Prometheus config templates and remote scrape job.
- `monitoring/loki/`: Loki config.
- `monitoring/promtail/`: Log scraping and parsing config.
- `monitoring/grafana/dashboards/`: Dashboard JSON.
- `docs/`: design, endpoint behavior, and troubleshooting.

## Important endpoint set

- `/`
- `/health.php`
- `/api/users.php`
- `/api/orders.php`
- `/api/payments.php`
- `/api/inventory.php`
- `/api/unstable.php`
- `/api/not-found-simulator.php`

## Full remote deployment guide

- `docs/04-two-machine-deployment.md`
- `docs/grafana-dashboard.md`

## Stop Machine A stack

```bash
docker compose down
```

To also remove volumes and all stored metric/log data:

```bash
docker compose down -v
```
