FROM php:8.2-apache

RUN a2enmod status headers rewrite

COPY apache/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY public/ /var/www/html/

RUN chown -R www-data:www-data /var/www/html
RUN mkdir -p /var/log/apache-real && chown -R www-data:www-data /var/log/apache-real

EXPOSE 80
