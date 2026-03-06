# 05 - Advanced PromQL Patterns

This chapter combines your jobs to answer higher-level operational questions.

## 1. Multi-Job Health Summary

Healthy target count by job:

```promql
sum by (job) (up == 1)
```

Down target count by job:

```promql
sum by (job) (up == 0)
```

## 2. Error Budget Style Query (Kubernetes API)

Success ratio over 30m:

```promql
1 - (
  sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster", code=~"5.."}[30m]))
  /
  sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster"}[30m]))
)
```

Sample output:

```text
{} 0.9971
```

## 3. Smoothing and Forecasting

Smoothed CPU (15m avg):

```promql
avg_over_time((100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode="idle"}[5m]))))[15m:1m])
```

Disk usage prediction 4h ahead:

```promql
predict_linear(node_filesystem_free_bytes{job="node_exporter", mountpoint="/"}[2h], 4 * 3600)
```

If result is negative, disk may fill before 4 hours.

## 4. Top-K and Outlier Detection

Top 5 pods by CPU:

```promql
topk(5, sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{job="kubernetes_gcp_cluster", image!="", container!="POD"}[5m])))
```

Noisy Prometheus handlers by latency p95:

```promql
topk(5, histogram_quantile(0.95, sum by (le, handler) (rate(prometheus_http_request_duration_seconds_bucket{job="prometheus"}[5m]))))
```

## 5. Join Example with `on` and `group_left`

Attach node label metadata to resource usage (example pattern):

```promql
sum by (node) (rate(container_cpu_usage_seconds_total{job="kubernetes_gcp_cluster", image!="", container!="POD"}[5m]))
* on(node) group_left(label_node_role_kubernetes_io_worker)
kube_node_labels{job="kubernetes_gcp_cluster"}
```

Use joins carefully because cardinality can grow quickly.

## 6. Recording Rule Candidates

Candidate 1:

```promql
record: instance:node_cpu_usage:ratio
expr: 1 - avg by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode="idle"}[5m]))
```

Candidate 2:

```promql
record: namespace:pod_cpu_usage:sum_rate5m
expr: sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{job="kubernetes_gcp_cluster", image!="", container!="POD"}[5m]))
```

Candidate 3:

```promql
record: job:up:sum
expr: sum by (job) (up)
```

## 7. Alert Rule Query Templates

Template: target down

```promql
up{job=~"kubernetes_gcp_cluster|node_exporter|prometheus"} == 0
```

Template: sustained high node CPU

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode="idle"}[5m]))) > 85
```

Template: deployment replicas unavailable

```promql
(kube_deployment_spec_replicas{job="kubernetes_gcp_cluster"} - kube_deployment_status_replicas_available{job="kubernetes_gcp_cluster"}) > 0
```
