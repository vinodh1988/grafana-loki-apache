<?php

declare(strict_types=1);

require_once __DIR__ . '/../_helpers.php';

$latency = randomSleep(50, 650);
maybeLogWarning('/api/inventory.php', 10);

$roll = random_int(1, 100);
if ($roll <= 12) {
    jsonResponse([
        'error' => 'Inventory item not found',
        'latency_ms' => $latency,
    ], 404);
    return;
}

jsonResponse([
    'endpoint' => 'inventory',
    'latency_ms' => $latency,
    'sku' => 'SKU-' . random_int(1000, 9999),
    'available_qty' => random_int(0, 200),
]);
