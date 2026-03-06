# How To Verify Everything Is Working

Use this as your single runbook after deployment.

Assumed architecture:
- Machine A: Apache app + apache-exporter + Loki + Promtail + loadgen (Docker)
- Machine B: Prometheus + Grafana (Linux services)

## 1. Machine A service health

Run on Machine A:

```bash
cd apache-project
docker compose ps -a
```

Expected:
- `apache-web` status is `Up (healthy)`
- `apache-exporter` status is `Up`
- `loki` status is `Up`
- `promtail` status is `Up`
- `apache-loadgen` status is `Up`

## 2. Application behavior check

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8088/health.php
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8088/api/not-found-simulator.php
for i in {1..10}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8088/api/unstable.php; done
```

Expected:
- `health.php` returns `200`
- `not-found-simulator.php` returns `404`
- `unstable.php` shows mixed statuses (`200`, `500`, `503`)

## 3. Apache exporter metrics check

```bash
curl -s http://localhost:9117/metrics | grep -E "^apache_" | head -n 30
```

Expected:
- Non-empty output with Apache metrics names

## 4. What metrics you should receive

You should see these core metric families from exporter:
- `apache_up`
- `apache_accesses_total`
- `apache_sent_kilobytes_total`
- `apache_workers`
- `apache_cpu_load`
- `apache_uptime_seconds_total`

If these exist and values are changing, metric ingestion is working.

## 5. Loki and Promtail pipeline check

```bash
docker compose logs --tail=120 loki
docker compose logs --tail=120 promtail
curl -s http://localhost:3100/ready
```

Expected:
- Loki ready endpoint prints `ready`
- Promtail logs do not show continuous `error creating promtail`
- No repeating `failed to start tailer` errors

## 6. Prometheus check on Machine B

Open:
- `http://<MACHINE_B_IP>:9090/targets`

Expected:
- target in job `apache_remote` is `UP`

Run queries in Prometheus UI:

```promql
up{job="apache_remote"}
rate(apache_accesses_total[1m])
apache_workers{state="busy"}
apache_cpu_load
```

Expected:
- first query returns `1`
- request rate is non-zero and fluctuating
- workers and CPU load show live values

## 7. Grafana datasource check on Machine B

In Grafana UI:
- `Connections -> Data sources`

Expected:
- Prometheus datasource test success
- Loki datasource test success

Required datasource settings:
- Prometheus URL: `http://localhost:9090`
- Loki URL: `http://<MACHINE_A_IP>:3100`
- UIDs: `prometheus` and `loki`

## 8. Grafana dashboard check

Open dashboard:
- `Apache Project - Metrics and Logs`

Expected panels:
- `Apache Up`: UP
- `Requests/sec`: moving line
- `Traffic (KB/sec)`: moving line
- `Status Code Rate by Status`: shows codes like `200`, `404`, `500`
- `Recent Error/Warn Logs`: recent log lines visible

## 9. One-shot all-green checklist

All of these must be true:
1. `docker compose ps -a` shows all five containers `Up`.
2. `curl http://localhost:9117/metrics` returns Apache metrics.
3. `curl http://localhost:3100/ready` returns `ready`.
4. Prometheus target `apache_remote` is `UP`.
5. Grafana dashboard shows both metric and log data.

## 10. If something is not working

Use this quick map:
- Missing metrics in Prometheus:
  - Check Machine B network access to `<MACHINE_A_IP>:9117`
  - Check `apache-exporter` logs
- Missing logs in Grafana:
  - Check Machine B network access to `<MACHINE_A_IP>:3100`
  - Check `promtail` logs for tailing errors
- Dashboard empty but data sources healthy:
  - Increase time range to `Last 30 minutes`
  - Confirm datasource UIDs match dashboard (`prometheus`, `loki`)
