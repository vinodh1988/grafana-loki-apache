# 06 - Troubleshooting and Cheat Sheet

Use this when a query returns empty results, wrong values, or unexpected spikes.

## 1. Fast Debug Flow

1. Check target health:

```promql
up{job=~"kubernetes_gcp_cluster|node_exporter|prometheus"}
```

2. Check metric existence:

```promql
count({__name__=~"node_.*"})
count({__name__=~"kube_.*"})
count({__name__=~"prometheus_.*"})
```

3. Check label set for the metric:

```promql
count by (job, instance) (node_cpu_seconds_total)
```

4. Expand time range in UI (for sparse data).

5. Remove filters and re-add labels one by one.

## 2. Common Issues

`No data`:

- Wrong `job` label value (`node exporter` vs `node_exporter`).
- Metric name mismatch across versions.
- Target is down (`up=0`).

`Spiky rate`:

- Increase range window (`[5m]` to `[10m]` or `[15m]`).
- Use `irate` only for very short, responsive views.

`Huge cardinality`:

- Avoid grouping by high-cardinality labels (pod UID, container ID).
- Use recording rules for repeated expensive queries.

`Division by zero`:

- Guard with `clamp_min(denominator, 1)` for safe ratios.

Example:

```promql
sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster", code=~"5.."}[5m])) / clamp_min(sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster"}[5m])), 1)
```

## 3. Query Tuning Tips

- Use `sum by (...)` before `topk` to reduce series count.
- Prefer `rate(counter[5m])` for stable alerting queries.
- Keep joins explicit with `on(...)`.
- Benchmark query cost in Prometheus expression browser.

## 4. API Query Examples (Optional)

Instant query:

```bash
curl -G http://localhost:9090/api/v1/query --data-urlencode 'query=sum by(job) (up)'
```

Range query:

```bash
curl -G http://localhost:9090/api/v1/query_range \
  --data-urlencode 'query=100 * (1 - avg by(instance) (rate(node_cpu_seconds_total{job="node_exporter",mode="idle"}[5m])))' \
  --data-urlencode 'start=2026-03-05T10:00:00Z' \
  --data-urlencode 'end=2026-03-05T11:00:00Z' \
  --data-urlencode 'step=30s'
```

## 5. Quick Query Cheat Sheet

Target availability:

```promql
up{job=~"kubernetes_gcp_cluster|node_exporter|prometheus"}
```

Node CPU percent:

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode="idle"}[5m])))
```

Node memory percent used:

```promql
100 * (1 - node_memory_MemAvailable_bytes{job="node_exporter"} / node_memory_MemTotal_bytes{job="node_exporter"})
```

Pod restarts in 30m:

```promql
sum by (namespace, pod) (increase(kube_pod_container_status_restarts_total{job="kubernetes_gcp_cluster"}[30m]))
```

Prometheus head series:

```promql
prometheus_tsdb_head_series{job="prometheus"}
```
