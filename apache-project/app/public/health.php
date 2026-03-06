<?php

declare(strict_types=1);

require_once __DIR__ . '/_helpers.php';

jsonResponse([
    'status' => 'ok',
    'service' => 'apache-project',
    'time' => gmdate('c'),
]);
