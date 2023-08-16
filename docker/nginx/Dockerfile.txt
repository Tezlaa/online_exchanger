FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY docker/nginx/nginx.conf /etc/nginx/conf.d
COPY docker/nginx/proxy-params.conf /etc/nginx
