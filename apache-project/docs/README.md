# Docs Output Verification Guide

Use this guide to quickly verify that your two-machine setup is working.

Architecture assumed:
- Machine A: Apache app + apache-exporter + Loki + Promtail + loadgen (Docker)
- Machine B: Prometheus + Grafana (Linux services)

## 1. Verify containers on Machine A

```bash
cd apache-project
docker compose ps
```

Expected:
- `web` is running
- `apache-exporter` is running
- `loki` is running
- `promtail` is running
- `loadgen` is running

## 2. Verify app endpoints on Machine A

Replace `<MACHINE_A_IP>` with actual IP.

```bash
curl -s http://<MACHINE_A_IP>:8088/ | jq .
curl -s -o /dev/null -w "%{http_code}\n" http://<MACHINE_A_IP>:8088/health.php
curl -s -o /dev/null -w "%{http_code}\n" http://<MACHINE_A_IP>:8088/api/unstable.php
curl -s -o /dev/null -w "%{http_code}\n" http://<MACHINE_A_IP>:8088/api/not-found-simulator.php
```

Expected:
- `/health.php` returns `200`
- `/api/unstable.php` varies (`200/500/503`)
- `/api/not-found-simulator.php` returns `404`

## 3. Verify Apache exporter on Machine A

```bash
curl -s http://<MACHINE_A_IP>:9117/metrics | grep -E "apache_accesses_total|apache_workers|apache_cpu_load" | head
```

Expected:
- Prometheus metrics are returned (non-empty output)

## 4. Verify Loki ingestion on Machine A

```bash
docker compose logs --tail=100 promtail
docker compose logs --tail=100 loki
```

Expected:
- No continuous connection/refused errors
- Promtail shows successful pushes to Loki

## 5. Verify Prometheus target on Machine B

Open Prometheus UI:
- `http://<MACHINE_B_IP>:9090/targets`

Expected:
- `job="apache_remote"` is `UP`

Query checks in Prometheus UI:

```promql
up{job="apache_remote"}
apache_accesses_total
apache_workers{state="busy"}
apache_cpu_load
```

Expected:
- Values are present and changing over time

## 6. Verify Grafana datasources on Machine B

In Grafana UI:
- `Connections -> Data sources`

Expected:
- Prometheus datasource test: success
- Loki datasource test: success

Datasource values should be:
- Prometheus URL: `http://localhost:9090`
- Loki URL: `http://<MACHINE_A_IP>:3100`
- UIDs: `prometheus` and `loki`

## 7. Verify dashboard output on Machine B

Open dashboard:
- `Apache Project - Metrics and Logs`

Expected panel behavior:
- `Apache Up`: `UP`
- `Busy Workers` / `Idle Workers`: numeric values
- `Requests/sec`: non-zero fluctuating line
- `Status Code Rate by Status`: multiple status series (`200`, `404`, `500`, etc.)
- `Recent Error/Warn Logs`: live warning/error log lines

## 8. Quick troubleshooting map

- Prometheus target down:
  - Check Machine B can reach `<MACHINE_A_IP>:9117`
  - Check `apache-exporter` container logs
- Loki datasource fails:
  - Check Machine B can reach `<MACHINE_A_IP>:3100`
  - Check `loki` and `promtail` logs
- Dashboard shows "No data":
  - Confirm datasource UIDs are exactly `prometheus` and `loki`
  - Increase dashboard time range to `Last 30 minutes`
  - Wait 1-2 minutes for loadgen traffic

## Related docs

- `docs/04-two-machine-deployment.md`
- `docs/how-to-check-working.md`
- `grafana-dashboard.md`
- `README.md`
