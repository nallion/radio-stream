<?php

$file = "mtproxy.txt";
$message = "";

// функция проверки прокси
function checkProxy($ip, $port, $timeout = 3) {
    $conn = @fsockopen($ip, $port, $errno, $errstr, $timeout);
    if ($conn) {
        fclose($conn);
        return true;
    }
    return false;
}

// обработка GET
if (isset($_GET['proxy'])) {

    $input = trim($_GET['proxy']);

    // формат ip:port:password
    if (preg_match('/^([\d\.]+):(\d+):([a-zA-Z0-9]+)$/', $input, $matches)) {

        $ip = $matches[1];
        $port = $matches[2];
        $pass = $matches[3];

        // проверка доступности
        if (checkProxy($ip, $port)) {

            $line = "$ip:$port:$pass\n";

            file_put_contents($file, $line, FILE_APPEND | LOCK_EX);

            $message = "✅ Прокси сохранён";
        } else {
            $message = "❌ Прокси недоступен";
        }

    } else {
        $message = "❌ Неверный формат (нужно ip:port:password)";
    }
}

?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Add MTProxy</title>
</head>
<body>

<h2>Добавить MTProxy</h2>

<form method="get">
    <input type="text" name="proxy" placeholder="ip:port:password" style="width:300px;">
    <button type="submit">Добавить</button>
</form>

<p><?php echo htmlspecialchars($message); ?></p>

</body>
</html>
