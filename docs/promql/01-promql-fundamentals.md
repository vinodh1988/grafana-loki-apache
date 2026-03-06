# 01 - PromQL Fundamentals

This chapter gives the core PromQL building blocks before job-specific usage.

## 1. Data Types

- Instant vector: set of time series with one sample each at eval time.
- Range vector: set of time series over a time window.
- Scalar: single numeric value.
- String: rarely used.

Example:

```promql
up{job="prometheus"}
```

Sample output:

```text
{job="prometheus", instance="10.42.0.5:9090"} 1
```

## 2. Selectors and Label Matchers

Exact match:

```promql
up{job="node_exporter"}
```

Regex match:

```promql
up{job=~"kubernetes_gcp_cluster|prometheus"}
```

Negative match:

```promql
up{job!="kubernetes_gcp_cluster"}
```

## 3. Time Windows

`[5m]` means look back 5 minutes.

```promql
rate(prometheus_http_requests_total[5m])
```

Sample output:

```text
{code="200", handler="/api/v1/query"} 1.74
{code="422", handler="/api/v1/query"} 0.01
```

## 4. Aggregations

`sum`, `avg`, `max`, `min`, `count`, `topk`, `bottomk`.

```promql
sum by (job) (up)
```

Sample output:

```text
{job="kubernetes_gcp_cluster"} 8
{job="node_exporter"} 6
{job="prometheus"} 1
```

## 5. Rates, Increases, and Gauges

Use `rate` for counters, direct values for gauges.

Counter example:

```promql
rate(node_network_receive_bytes_total{job="node_exporter"}[5m])
```

Gauge example:

```promql
node_memory_MemAvailable_bytes{job="node_exporter"}
```

## 6. Useful Operators

Arithmetic:

```promql
100 * (1 - node_memory_MemAvailable_bytes{job="node_exporter"} / node_memory_MemTotal_bytes{job="node_exporter"})
```

Comparison:

```promql
up{job="kubernetes_gcp_cluster"} == 0
```

Logical set operators (`and`, `or`, `unless`) are useful for joins and filtering.

## 7. Label Grouping Basics

```promql
sum by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode!="idle"}[5m]))
```

Sample output:

```text
{instance="10.42.1.10:9100"} 1.24
{instance="10.42.1.11:9100"} 0.83
```

## 8. First Dashboard-Ready Queries

Total healthy targets by job:

```promql
sum by (job) (up == 1)
```

Targets down right now:

```promql
up == 0
```

Top 5 busiest CPU nodes:

```promql
topk(5, sum by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode!="idle"}[5m])))
```
