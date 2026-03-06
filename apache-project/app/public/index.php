<?php

declare(strict_types=1);

require_once __DIR__ . '/_helpers.php';

$latency = randomSleep(20, 350);
maybeLogWarning('/');

jsonResponse([
    'service' => 'apache-project',
    'message' => 'Apache test service is running',
    'latency_ms' => $latency,
    'timestamp' => gmdate('c'),
    'endpoints' => [
        '/health.php',
        '/api/users.php',
        '/api/orders.php',
        '/api/payments.php',
        '/api/inventory.php',
        '/api/unstable.php',
        '/api/not-found-simulator.php',
    ],
]);
