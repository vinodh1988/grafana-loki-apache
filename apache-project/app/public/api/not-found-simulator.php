<?php

declare(strict_types=1);

require_once __DIR__ . '/../_helpers.php';

$latency = randomSleep(30, 300);
http_response_code(404);
header('Content-Type: application/json');

echo json_encode([
    'error' => 'Synthetic not found endpoint',
    'latency_ms' => $latency,
    'why' => 'Used to generate predictable 404 access logs',
], JSON_PRETTY_PRINT);
