<?php

$url = "https://raw.githubusercontent.com/SoliSpirit/mtproto/refs/heads/master/all_proxies.txt";

$data = file($url, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

$result = [];

foreach ($data as $line) {

    $query = parse_url($line, PHP_URL_QUERY);
    parse_str($query, $p);

    if (isset($p['server'], $p['port'], $p['secret'])) {
        $result[] = $p['server'] . ":" . $p['port'] . ":" . $p['secret'];
    }
}

// Перемешиваем
shuffle($result);

// Выводим
foreach ($result as $line) {
    echo $line . PHP_EOL;
}
