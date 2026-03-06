# Grafana Alerting UI Guide (No Provisioning YAML)

This file intentionally uses only Grafana UI steps.

## 1. Create webhook contact point

1. Open Grafana.
2. Go to `Alerting -> Contact points`.
3. Click `New contact point`.
4. Name: `python-webhook`.
5. Integration type: `Webhook`.
6. URL: `http://<WEBHOOK_HOST>:5001/grafana`.
7. HTTP Method: `POST`.
8. Save contact point.

## 2. Create notification policy

1. Go to `Alerting -> Notification policies`.
2. Edit the default policy or add child policy.
3. Matchers (recommended):
   - `source = grafana-alerts`
4. Contact point: `python-webhook`.
5. Save policy.

## 3. Create Grafana alert rule

1. Go to `Alerting -> Alert rules`.
2. Click `New alert rule`.
3. Rule name: `GrafanaSignalAboveDynamicThreshold`.
4. Data source: your Prometheus datasource.
5. Query A:
   - `custom_signal_value`
6. Query B:
   - `custom_threshold_value`
7. Expression C (Math):
   - `$A > $B`
8. Condition:
   - Trigger when C is true for `15s`.
9. Labels:
   - `severity=warning`
   - `source=grafana-alerts`
10. Annotations:
   - summary: `Grafana detected signal above threshold`
11. Save and enable.

## 4. Optional critical rule

Create another rule named `GrafanaSignalCritical`:
- Query A: `custom_signal_value`
- Query B: `custom_threshold_value`
- Expression: `$A > ($B * 1.5)`
- For: `30s`
- Labels: `severity=critical`, `source=grafana-alerts`

## 5. Verify delivery

1. Use `Test` button on contact point to send a sample notification.
2. Confirm webhook terminal shows `[GRAFANA] ...` log entry.
3. Confirm `webhook/alerts.log` has `"source": "grafana"` entries.
