# Prometheus and Grafana Queries

## Core Prometheus metrics

- Requests per second:

```promql
sum(rate(apache_accesses_total[1m]))
```

- Busy workers:

```promql
max(apache_workers{state="busy"})
```

- Idle workers:

```promql
max(apache_workers{state="idle"})
```

- CPU load:

```promql
max(apache_cpu_load)
```

## LogQL examples

- Status code rate by status:

```logql
sum by (status) (
  rate(
    {job="apache_access"}
    | pattern "<ip> <ident> <user> [<ts>] \"<method> <path> <proto>\" <status> <bytes> <duration> \"<referrer>\" \"<agent>\""
    [1m]
  )
)
```

- Error volume by parsed level:

```logql
sum by (level) (
  count_over_time(
    {job="apache_error"}
    | regexp "\\] \\[(?P<level>[^\\]]+)\\]"
    [5m]
  )
)
```

- p95 request duration from access logs (ms):

```logql
quantile_over_time(
  0.95,
  {job="apache_access"}
  | pattern "<ip> <ident> <user> [<ts>] \"<method> <path> <proto>\" <status> <bytes> <duration> \"<referrer>\" \"<agent>\""
  | unwrap duration
  [5m]
) / 1000
```
