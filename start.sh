#!/bin/bash

REPO=https://github.com/nallion/radio-stream
BRANCH=main
DIR=/var/www/html

# очищаем папку
rm -rf $DIR/*

# Клонируем или обновляем
if [ ! -d "$DIR/.git" ]; then
    git clone --depth=1 -b $BRANCH $REPO $DIR
else
    cd $DIR
    git pull
fi

#Права на файл
chmod 777 /var/www/html/mtproxy.txt
# Запуск php-fpm
php-fpm -D

# запуск nginx
nginx -g "daemon off;"
