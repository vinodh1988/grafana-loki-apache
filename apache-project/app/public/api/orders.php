<?php

declare(strict_types=1);

require_once __DIR__ . '/../_helpers.php';

$latency = randomSleep(70, 1300);
maybeLogWarning('/api/orders.php', 25);

$roll = random_int(1, 100);
if ($roll <= 10) {
    error_log('Synthetic timeout tendency in /api/orders.php');
    jsonResponse([
        'error' => 'Order gateway timeout',
        'latency_ms' => $latency,
    ], 504);
    return;
}
if ($roll <= 20) {
    jsonResponse([
        'error' => 'Invalid order payload',
        'latency_ms' => $latency,
    ], 400);
    return;
}

jsonResponse([
    'endpoint' => 'orders',
    'latency_ms' => $latency,
    'order_count' => random_int(2, 30),
    'sample_order' => [
        'order_id' => 'ORD-' . random_int(10000, 99999),
        'status' => 'processed',
    ],
]);
