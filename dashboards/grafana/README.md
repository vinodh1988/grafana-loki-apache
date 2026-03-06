# Grafana Dashboards (Separate)

These dashboards are tailored for your Prometheus jobs:

- `node-exporter-dashboard.json` for `job="node_exporter"`
- `kubernetes-dashboard.json` for `job="kubernetes_gcp_cluster"`

## Import Steps

1. Open Grafana.
2. Go to `Dashboards` -> `New` -> `Import`.
3. Upload one JSON file.
4. Select your Prometheus datasource when prompted.
5. Click `Import`.

## Notes

- Node dashboard has an `instance` variable.
- Kubernetes dashboard has a `namespace` variable.
- Both dashboards assume the exact job labels:
  - `node_exporter`
  - `kubernetes_gcp_cluster`

If your job labels differ, replace `job="..."` in the panel queries.
