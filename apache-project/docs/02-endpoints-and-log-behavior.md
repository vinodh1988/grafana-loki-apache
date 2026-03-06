# Endpoint and Log Behavior

## Endpoints

- `/`: service info and endpoint list.
- `/health.php`: always healthy check.
- `/api/users.php`: mostly successful, occasional `500`.
- `/api/orders.php`: mixed `200`, `400`, `504`.
- `/api/payments.php`: mixed `200`, `429`, `500`.
- `/api/inventory.php`: mixed `200`, `404`.
- `/api/unstable.php`: high-chaos endpoint with warnings/errors and `500`/`503`.
- `/api/not-found-simulator.php`: deterministic `404`.

## Access log format

Configured in `app/apache/000-default.conf` with request duration (`%D`) included:

- `%>s` status code
- `%b` response size
- `%D` request duration in microseconds

This makes latency and status analysis possible directly from logs.

## Error log behavior

The app intentionally emits:

- `E_USER_WARNING` via `trigger_error(...)`.
- application errors via `error_log(...)`.

These produce warning/error entries that can be queried in Loki and visualized in Grafana.
