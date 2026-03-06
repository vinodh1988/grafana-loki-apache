# End-to-End Test Scenarios

## Scenario A: Trigger warning

```bash
curl -X POST "http://localhost:9108/set?value=30"
curl -X POST "http://localhost:9108/threshold?value=70"
curl -X POST "http://localhost:9108/spike?delta=50"
```

Expected:
- Prometheus warning alert fires after ~15s.
- Alertmanager posts to `/alertmanager`.
- Grafana warning rule posts to `/grafana`.

## Scenario B: Trigger critical

```bash
curl -X POST "http://localhost:9108/spike?delta=100"
```

Expected:
- Critical alert fires after configured `for` duration.
- Webhook receives critical payloads from both sources.

## Scenario C: Dynamic threshold drop

```bash
curl -X POST "http://localhost:9108/set?value=60"
curl -X POST "http://localhost:9108/threshold?value=20"
```

Expected:
- Alerting triggers quickly because threshold collapses.

## Scenario D: Drastic variation mode

```bash
curl -X POST "http://localhost:9108/mode?name=chaos"
sleep 60
curl -X POST "http://localhost:9108/mode?name=manual"
```

Expected:
- Alert transitions across inactive/pending/firing/resolved states.
- Useful for stress-testing webhook handling.

## Run full scripted demo

```bash
cd grafana-alerts/scripts
chmod +x demo-spikes.sh
./demo-spikes.sh
```

## Inspect alert logs

```bash
tail -f grafana-alerts/webhook/alerts.log
```

Look for both:
- `"source": "alertmanager"`
- `"source": "grafana"`
