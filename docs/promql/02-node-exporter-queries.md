# 02 - Node Exporter PromQL Queries

This chapter focuses on Linux host metrics from `job="node_exporter"`.

## 1. Node Health

Is the node exporter reachable?

```promql
up{job="node_exporter"}
```

Sample output:

```text
{instance="10.42.1.10:9100", job="node_exporter"} 1
{instance="10.42.1.11:9100", job="node_exporter"} 1
```

## 2. CPU Usage

Overall CPU usage percent per node:

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode="idle"}[5m])))
```

Sample output:

```text
{instance="10.42.1.10:9100"} 62.4
{instance="10.42.1.11:9100"} 48.9
```

Top nodes by non-idle CPU:

```promql
topk(3, sum by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode!="idle"}[5m])))
```

## 3. Memory Usage

Memory used percentage:

```promql
100 * (1 - (node_memory_MemAvailable_bytes{job="node_exporter"} / node_memory_MemTotal_bytes{job="node_exporter"}))
```

Sample output:

```text
{instance="10.42.1.10:9100"} 73.1
{instance="10.42.1.11:9100"} 58.7
```

Low available memory alert candidate:

```promql
(node_memory_MemAvailable_bytes{job="node_exporter"} / node_memory_MemTotal_bytes{job="node_exporter"}) < 0.1
```

## 4. Disk Space and IO

Filesystem usage percent (real disks):

```promql
100 * (1 - (node_filesystem_avail_bytes{job="node_exporter", fstype!~"tmpfs|overlay", mountpoint!~"/run.*"} / node_filesystem_size_bytes{job="node_exporter", fstype!~"tmpfs|overlay", mountpoint!~"/run.*"}))
```

Sample output:

```text
{instance="10.42.1.10:9100", mountpoint="/"} 81.2
{instance="10.42.1.11:9100", mountpoint="/"} 64.5
```

Disk read throughput:

```promql
sum by (instance, device) (rate(node_disk_read_bytes_total{job="node_exporter"}[5m]))
```

Disk write throughput:

```promql
sum by (instance, device) (rate(node_disk_written_bytes_total{job="node_exporter"}[5m]))
```

## 5. Network Throughput

Receive bytes/sec:

```promql
sum by (instance) (rate(node_network_receive_bytes_total{job="node_exporter", device!="lo"}[5m]))
```

Transmit bytes/sec:

```promql
sum by (instance) (rate(node_network_transmit_bytes_total{job="node_exporter", device!="lo"}[5m]))
```

Sample output:

```text
{instance="10.42.1.10:9100"} 1350000
{instance="10.42.1.11:9100"} 920000
```

## 6. Node Reboots and Uptime

Node uptime (seconds):

```promql
time() - node_boot_time_seconds{job="node_exporter"}
```

Reboot detection (boot time changed in last hour):

```promql
changes(node_boot_time_seconds{job="node_exporter"}[1h]) > 0
```

## 7. Practical Alert Query Set

High CPU for 10m:

```promql
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{job="node_exporter", mode="idle"}[5m]))) > 85
```

High memory usage:

```promql
100 * (1 - (node_memory_MemAvailable_bytes{job="node_exporter"} / node_memory_MemTotal_bytes{job="node_exporter"})) > 90
```

Low disk free:

```promql
(node_filesystem_avail_bytes{job="node_exporter", fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{job="node_exporter", fstype!~"tmpfs|overlay"}) < 0.1
```
