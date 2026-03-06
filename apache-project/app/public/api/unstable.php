<?php

declare(strict_types=1);

require_once __DIR__ . '/../_helpers.php';

$latency = randomSleep(200, 3000);
$roll = random_int(1, 100);

if ($roll <= 18) {
    trigger_error('Synthetic warning from unstable endpoint', E_USER_WARNING);
}
if ($roll <= 35) {
    error_log('Synthetic critical-like error from unstable endpoint');
    jsonResponse([
        'error' => 'Unstable endpoint failure',
        'latency_ms' => $latency,
        'hint' => 'Designed for error and warning generation',
    ], 500);
    return;
}
if ($roll <= 50) {
    jsonResponse([
        'error' => 'Service unavailable spike',
        'latency_ms' => $latency,
    ], 503);
    return;
}

jsonResponse([
    'endpoint' => 'unstable',
    'latency_ms' => $latency,
    'state' => 'ok-but-chaotic',
    'roll' => $roll,
]);
