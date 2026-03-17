<?php

$file = "mtproxy.txt";

if (!file_exists($file)) {
    die("Файл не найден");
}

$handle = fopen($file, "r");

while (($line = fgets($handle)) !== false) {
    echo htmlspecialchars($line) . "\r\n";
}

fclose($handle);
