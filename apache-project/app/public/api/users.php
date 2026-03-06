<?php

declare(strict_types=1);

require_once __DIR__ . '/../_helpers.php';

$latency = randomSleep(40, 900);
maybeLogWarning('/api/users.php', 20);

if (maybeLogError('/api/users.php', 6)) {
    jsonResponse([
        'error' => 'User service temporary failure',
        'latency_ms' => $latency,
    ], 500);
    return;
}

jsonResponse([
    'endpoint' => 'users',
    'latency_ms' => $latency,
    'users' => [
        ['id' => 101, 'name' => 'Asha Rao'],
        ['id' => 102, 'name' => 'Noah Carter'],
        ['id' => 103, 'name' => 'Priya Menon'],
    ],
]);
