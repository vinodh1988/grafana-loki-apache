# 03 - Kubernetes Job PromQL Queries

This chapter assumes Kubernetes metrics are exposed under `job="kubernetes_gcp_cluster"`.
Depending on your stack, metric names can come from kube-state-metrics, cAdvisor, kubelet, or API server scrape endpoints.

## 1. Target Health for Kubernetes Job

```promql
up{job="kubernetes_gcp_cluster"}
```

Sample output:

```text
{job="kubernetes_gcp_cluster", instance="10.42.0.15:8080"} 1
{job="kubernetes_gcp_cluster", instance="10.42.0.16:8080"} 1
```

## 2. Pod Restarts (Counter)

Restarts in the last 30 minutes:

```promql
sum by (namespace, pod) (increase(kube_pod_container_status_restarts_total{job="kubernetes_gcp_cluster"}[30m]))
```

Sample output:

```text
{namespace="payments", pod="api-7dd4f79f6f-8lkmz"} 2
{namespace="default", pod="worker-6f6d8d9fbc-2f7px"} 0
```

Pods with frequent restarts (>3 in 30m):

```promql
sum by (namespace, pod) (increase(kube_pod_container_status_restarts_total{job="kubernetes_gcp_cluster"}[30m])) > 3
```

## 3. Running vs Desired Pods

Desired replicas:

```promql
sum by (namespace, deployment) (kube_deployment_spec_replicas{job="kubernetes_gcp_cluster"})
```

Available replicas:

```promql
sum by (namespace, deployment) (kube_deployment_status_replicas_available{job="kubernetes_gcp_cluster"})
```

Replica gap query:

```promql
sum by (namespace, deployment) (kube_deployment_spec_replicas{job="kubernetes_gcp_cluster"}) - sum by (namespace, deployment) (kube_deployment_status_replicas_available{job="kubernetes_gcp_cluster"})
```

Sample output:

```text
{namespace="payments", deployment="api"} 1
{namespace="default", deployment="frontend"} 0
```

## 4. Pod CPU and Memory (Container Level)

CPU usage per pod (cores):

```promql
sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{job="kubernetes_gcp_cluster", image!="", container!="POD"}[5m]))
```

Memory working set per pod (bytes):

```promql
sum by (namespace, pod) (container_memory_working_set_bytes{job="kubernetes_gcp_cluster", image!="", container!="POD"})
```

Sample output:

```text
{namespace="payments", pod="api-7dd4f79f6f-8lkmz"} 0.23
{namespace="payments", pod="api-7dd4f79f6f-j2s9n"} 0.19
```

## 5. Node Pressure Signals (From Kubernetes Metrics)

Unschedulable nodes:

```promql
kube_node_spec_unschedulable{job="kubernetes_gcp_cluster"} == 1
```

NotReady nodes:

```promql
kube_node_status_condition{job="kubernetes_gcp_cluster", condition="Ready", status="true"} == 0
```

## 6. API Server Request Rate and Errors

API requests/sec:

```promql
sum by (verb, resource) (rate(apiserver_request_total{job="kubernetes_gcp_cluster"}[5m]))
```

API error ratio (5xx):

```promql
sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster", code=~"5.."}[5m])) / sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster"}[5m]))
```

Sample output:

```text
{} 0.0042
```

## 7. Namespace Capacity View

CPU usage by namespace:

```promql
sum by (namespace) (rate(container_cpu_usage_seconds_total{job="kubernetes_gcp_cluster", image!="", container!="POD"}[5m]))
```

Memory usage by namespace:

```promql
sum by (namespace) (container_memory_working_set_bytes{job="kubernetes_gcp_cluster", image!="", container!="POD"})
```

## 8. Practical Alert Query Set

CrashLoop-like behavior (restarts):

```promql
sum by (namespace, pod) (increase(kube_pod_container_status_restarts_total{job="kubernetes_gcp_cluster"}[10m])) > 2
```

Deployment unavailable replicas:

```promql
(kube_deployment_spec_replicas{job="kubernetes_gcp_cluster"} - kube_deployment_status_replicas_available{job="kubernetes_gcp_cluster"}) > 0
```

High API server 5xx ratio:

```promql
(sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster", code=~"5.."}[5m])) / sum(rate(apiserver_request_total{job="kubernetes_gcp_cluster"}[5m]))) > 0.02
```
