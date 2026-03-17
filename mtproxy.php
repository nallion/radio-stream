<?php

$file = "mtproxy.txt";

if (!file_exists($file)) {
    die("Файл не найден");
}

$handle = fopen($file, "r");

while (($line = fgets($handle)) !== false) {
    echo htmlspecialchars($line) . "<br>";
}

fclose($handle);
