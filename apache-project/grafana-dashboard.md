# Grafana Dashboard Setup (Machine B Service Install)

This document is for your setup where Grafana runs as a Linux service on a different machine than Apache/Loki.

## Files in this project

- Dashboard JSON:
  - `monitoring/grafana/dashboards/apache-observability-dashboard.json`
- Datasource provisioning template:
  - `monitoring/grafana/provisioning/datasources/datasource.yml`
- Dashboard provider provisioning template:
  - `monitoring/grafana/provisioning/dashboards/dashboard.yml`

## Option 1: Fast manual method (recommended first)

Use this once to get everything working quickly.

1. Add datasources in Grafana UI (`Connections -> Data sources`).
2. Create Prometheus datasource:
   - Name: `Prometheus`
   - URL: `http://localhost:9090`
   - UID: `prometheus`
3. Create Loki datasource:
   - Name: `Loki`
   - URL: `http://<APACHE_LOKI_HOST>:3100`
   - UID: `loki`
4. Import dashboard JSON:
   - `Dashboards -> Import`
   - Upload `monitoring/grafana/dashboards/apache-observability-dashboard.json`

Why UID matters:
- Dashboard panels reference datasource UIDs directly.
- If UIDs differ, panels show datasource errors.

## Option 2: Full provisioning method (automatic on Grafana startup)

Use this when you want dashboard and datasources managed as files.

### 1. Copy datasource provisioning file

Copy project file:
- From: `monitoring/grafana/provisioning/datasources/datasource.yml`
- To: `/etc/grafana/provisioning/datasources/datasource.yml`

Edit `url` values in destination file:
- Prometheus: `http://localhost:9090`
- Loki: `http://<APACHE_LOKI_HOST>:3100`

### 2. Copy dashboard provider file

Copy project file:
- From: `monitoring/grafana/provisioning/dashboards/dashboard.yml`
- To: `/etc/grafana/provisioning/dashboards/dashboard.yml`

### 3. Copy dashboard JSON to Grafana dashboard path

By default, `dashboard.yml` points to:
- `/var/lib/grafana/dashboards`

So copy JSON:
- From: `monitoring/grafana/dashboards/apache-observability-dashboard.json`
- To: `/var/lib/grafana/dashboards/apache-observability-dashboard.json`

### 4. Ensure Grafana service user can read files

Typical service user is `grafana`.

Example:

```bash
sudo chown -R grafana:grafana /etc/grafana/provisioning
sudo chown -R grafana:grafana /var/lib/grafana/dashboards
sudo chmod -R 755 /etc/grafana/provisioning
sudo chmod -R 755 /var/lib/grafana/dashboards
```

### 5. Restart Grafana

```bash
sudo systemctl restart grafana-server
sudo systemctl status grafana-server --no-pager
```

## How `datasource.yml` is utilized

Grafana reads `/etc/grafana/provisioning/datasources/*.yml` during startup.

In this project, `datasource.yml` defines:
- a Prometheus datasource with UID `prometheus`
- a Loki datasource with UID `loki`

Effect:
- Datasources are auto-created (or reconciled) on Grafana startup.
- Dashboard panels bind correctly by UID without manual remapping.

## How `dashboard.yml` is utilized

Grafana reads `/etc/grafana/provisioning/dashboards/*.yml` during startup.

In this project, `dashboard.yml` defines a file provider that scans:
- `/var/lib/grafana/dashboards`

Effect:
- Any dashboard JSON in that folder is auto-imported.
- Updates to JSON are reloaded based on `updateIntervalSeconds`.

## Validation checklist

1. Datasources status is green in Grafana UI.
2. Prometheus query test works:
   - `up{job="apache_remote"}`
3. Loki query test works:
   - `{job="apache_access"}`
4. Dashboard opens with panels populated.

## Common issues

- Panel says datasource not found:
  - UID mismatch; set UIDs exactly `prometheus` and `loki`.
- Loki datasource fails:
  - Network/firewall from Grafana host to `<APACHE_LOKI_HOST>:3100`.
- Dashboard not auto-loaded:
  - Wrong path in `dashboard.yml` or JSON not copied to `/var/lib/grafana/dashboards`.
- Provisioning changes not visible:
  - Restart `grafana-server` after editing provisioning files.
