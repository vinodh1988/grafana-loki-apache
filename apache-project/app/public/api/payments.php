<?php

declare(strict_types=1);

require_once __DIR__ . '/../_helpers.php';

$latency = randomSleep(100, 1800);
maybeLogWarning('/api/payments.php', 30);

$roll = random_int(1, 100);
if ($roll <= 8) {
    error_log('Synthetic payment DB lock in /api/payments.php');
    jsonResponse([
        'error' => 'Database lock timeout',
        'latency_ms' => $latency,
    ], 500);
    return;
}
if ($roll <= 20) {
    jsonResponse([
        'error' => 'Rate limit reached for payment API',
        'latency_ms' => $latency,
    ], 429);
    return;
}

jsonResponse([
    'endpoint' => 'payments',
    'latency_ms' => $latency,
    'transaction_id' => 'TX-' . random_int(100000, 999999),
    'status' => 'approved',
]);
