# Architecture

## Machine split

- Machine A: `web`, `apache-exporter`, `loki`, `promtail`, `loadgen` (Docker)
- Machine B: `prometheus`, `grafana` (Linux services)

## Data flow

1. `loadgen` sends fluctuating random traffic to Apache endpoints.
2. Apache writes access logs and error logs.
3. `apache_exporter` reads Apache `mod_status` and exposes Prometheus metrics.
4. Prometheus scrapes Apache exporter metrics.
5. Promtail tails Apache logs and ships them to Loki.
6. Grafana reads metrics from Prometheus and logs from Loki.

## Services on Machine A

- `web`: Apache + PHP endpoint service.
- `apache-exporter`: exposes Apache metrics in Prometheus format.
- `loki`: log storage/query backend.
- `promtail`: log collector/parser.
- `loadgen`: random workload generator.

## Services on Machine B

- `prometheus`: metrics database and scrape engine.
- `grafana`: visualization and log analytics UI.

## Why this setup is useful

- Produces diverse traffic and response outcomes.
- Helps practice metric-driven analysis and log correlation.
- Simulates warning/error spikes for realistic dashboard validation.
