<?php
$file = "mtproxy.txt";

if (!file_exists($file)) {
    die("Файл не найден");
}

// Читаем строки
$lines = file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

if (!$lines) {
    die("Файл пуст или не удалось прочитать");
}

// Перемешиваем
shuffle($lines);

// Выводим с обычным переносом строки
foreach ($lines as $line) {
    echo $line . PHP_EOL;
}
?>
