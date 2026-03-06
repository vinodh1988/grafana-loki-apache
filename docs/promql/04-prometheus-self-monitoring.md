# 04 - Prometheus Self-Monitoring Queries

This chapter focuses on `job="prometheus"` so you can monitor Prometheus itself.

## 1. Is Prometheus Up

```promql
up{job="prometheus"}
```

Sample output:

```text
{instance="10.42.0.5:9090", job="prometheus"} 1
```

## 2. Scrape Duration and Health

Scrape duration by target:

```promql
scrape_duration_seconds
```

95th percentile scrape duration over 5m:

```promql
histogram_quantile(0.95, sum by (le, job) (rate(scrape_duration_seconds_bucket[5m])))
```

Targets frequently failing scrapes:

```promql
sum by (job, instance) (increase(prometheus_target_scrapes_exceeded_sample_limit_total{job="prometheus"}[15m]))
```

## 3. Rule Evaluation Performance

Rule group evaluation duration:

```promql
prometheus_rule_group_last_duration_seconds{job="prometheus"}
```

Rules missing schedule (slow evaluations):

```promql
prometheus_rule_group_iterations_missed_total{job="prometheus"}
```

Sample output:

```text
{rule_group="node-alerts", file="/etc/prometheus/rules/node.yml"} 0
{rule_group="k8s-alerts", file="/etc/prometheus/rules/k8s.yml"} 3
```

## 4. Query Performance

Queries per second by handler:

```promql
sum by (handler) (rate(prometheus_http_requests_total{job="prometheus"}[5m]))
```

95th percentile API latency:

```promql
histogram_quantile(0.95, sum by (le, handler) (rate(prometheus_http_request_duration_seconds_bucket{job="prometheus"}[5m])))
```

## 5. TSDB Health

Head series count:

```promql
prometheus_tsdb_head_series{job="prometheus"}
```

WAL fsync duration p95:

```promql
histogram_quantile(0.95, sum by (le) (rate(prometheus_tsdb_wal_fsync_duration_seconds_bucket{job="prometheus"}[5m])))
```

Compaction duration p95:

```promql
histogram_quantile(0.95, sum by (le) (rate(prometheus_tsdb_compaction_duration_seconds_bucket{job="prometheus"}[15m])))
```

Sample output:

```text
{job="prometheus"} 0.184
```

## 6. Ingestion and Samples

Samples appended rate:

```promql
rate(prometheus_tsdb_head_samples_appended_total{job="prometheus"}[5m])
```

Samples dropped rate:

```promql
rate(prometheus_target_scrapes_sample_out_of_order_total{job="prometheus"}[5m])
```

## 7. Retention and Storage Signals

Prometheus memory usage:

```promql
process_resident_memory_bytes{job="prometheus"}
```

Filesystem free ratio on Prometheus host (if node exporter covers same host):

```promql
node_filesystem_avail_bytes{job="node_exporter", mountpoint="/"} / node_filesystem_size_bytes{job="node_exporter", mountpoint="/"}
```

## 8. Practical Alert Query Set

Prometheus target down:

```promql
up{job="prometheus"} == 0
```

Rule evaluations are missing:

```promql
increase(prometheus_rule_group_iterations_missed_total{job="prometheus"}[10m]) > 0
```

High TSDB churn warning:

```promql
rate(prometheus_tsdb_head_series_created_total{job="prometheus"}[5m]) - rate(prometheus_tsdb_head_series_removed_total{job="prometheus"}[5m]) > 20000
```
