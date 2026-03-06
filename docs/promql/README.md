# PromQL Tutorial for Your 3 Jobs

This guide is tailored for these Prometheus scrape jobs:

- `kubernetes_gcp_cluster`
- `node_exporter`
- `prometheus`

It is written as a practical, query-first tutorial with sample outputs.

## Recommended Learning Order

1. `01-promql-fundamentals.md`
2. `02-node-exporter-queries.md`
3. `03-kubernetes-queries.md`
4. `04-prometheus-self-monitoring.md`
5. `05-advanced-promql-patterns.md`
6. `06-troubleshooting-cheatsheet.md`

## Assumptions

- Prometheus is running and scraping all three jobs.
- Metric names may vary slightly by exporters and versions.
- You can run queries in Prometheus UI at `/graph`.

## How to Read Sample Output

Most examples show one of these formats:

- Instant vector (current value)
- Range vector transformed into scalar/vector (`rate`, `increase`, `avg_over_time`)
- Table-like short output for readability

Sample values are realistic but illustrative.

## Verify Targets First

Run this query to confirm target health:

```promql
up
```

Sample output:

```text
{job="kubernetes_gcp_cluster", instance="10.42.0.15:8080"} 1
{job="node_exporter", instance="10.42.1.10:9100"} 1
{job="prometheus", instance="10.42.0.5:9090"} 1
```

If any target shows `0`, jump to `06-troubleshooting-cheatsheet.md`.
