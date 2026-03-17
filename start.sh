#!/bin/bash

REPO=https://github.com/nallion/radio-stream
BRANCH=main
DIR=/var/www/html

# Клонируем или обновляем
if [ ! -d "$DIR/.git" ]; then
    git clone --depth=1 -b $BRANCH $REPO $DIR
else
    cd $DIR
    git pull
fi

# Запуск php-fpm
php-fpm -D

# запуск nginx
nginx -g "daemon off;"
