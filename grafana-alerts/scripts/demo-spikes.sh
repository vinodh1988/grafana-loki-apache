#!/usr/bin/env bash
set -euo pipefail

EXPORTER_BASE_URL="${EXPORTER_BASE_URL:-http://localhost:9108}"

echo "1) Reset to normal"
curl -s -X POST "${EXPORTER_BASE_URL}/set?value=30" >/dev/null
curl -s -X POST "${EXPORTER_BASE_URL}/threshold?value=70" >/dev/null
curl -s -X POST "${EXPORTER_BASE_URL}/mode?name=manual" >/dev/null

echo "2) Warning-level breach"
curl -s -X POST "${EXPORTER_BASE_URL}/spike?delta=50" >/dev/null
sleep 20

echo "3) Critical-level breach"
curl -s -X POST "${EXPORTER_BASE_URL}/spike?delta=70" >/dev/null
sleep 35

echo "4) Return to normal"
curl -s -X POST "${EXPORTER_BASE_URL}/set?value=25" >/dev/null
curl -s -X POST "${EXPORTER_BASE_URL}/threshold?value=80" >/dev/null

echo "5) Chaos mode for drastic variation"
curl -s -X POST "${EXPORTER_BASE_URL}/mode?name=chaos" >/dev/null
sleep 60

curl -s -X POST "${EXPORTER_BASE_URL}/mode?name=manual" >/dev/null
echo "Done"
