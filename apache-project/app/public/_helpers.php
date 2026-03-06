<?php

declare(strict_types=1);

function jsonResponse(array $payload, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json');
    echo json_encode($payload, JSON_PRETTY_PRINT);
}

function randomSleep(int $minMs, int $maxMs): int
{
    $delay = random_int($minMs, $maxMs);
    usleep($delay * 1000);
    return $delay;
}

function maybeLogWarning(string $endpoint, int $chancePercent = 15): void
{
    if (random_int(1, 100) <= $chancePercent) {
        trigger_error("Simulated warning at {$endpoint}", E_USER_WARNING);
    }
}

function maybeLogError(string $endpoint, int $chancePercent = 8): bool
{
    if (random_int(1, 100) <= $chancePercent) {
        error_log("Simulated application error at {$endpoint}");
        return true;
    }

    return false;
}
