FROM php:8.2-fpm

# Устанавливаем nginx и git
RUN apt-get update && apt-get install -y \
    nginx \
    git \
    && rm -rf /var/lib/apt/lists/*

# Папка сайта
WORKDIR /var/www

# Копируем конфиг nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Скрипт запуска
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]
