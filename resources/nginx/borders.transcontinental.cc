upstream borders {
    server unix:///opt/borders/server.sock
    # server 127.0.0.1:8000;
    # keepalive 8;
}

server {
    listen 81;

    server_name borders.transcontinental.cc;
    charset utf-8;

    access_log /var/log/nginx/borders.transcontinental.cc-access.log;
    error_log /var/log/nginx/borders.transcontinental.cc-errors.log;

    client_max_body_size 75M;

    # location /media {
    #   alias /path/to/your/mysite/media;  # your Django project's media files - amend as required
    # }

    location /static {
        alias /opt/borders/borders.transcontinental.cc/www/collected-static;
    }

    location / {
        uwsgi_pass  borders;
        include     /opt/borders/borders.transcontinental.cc/resources/nginx/uwsgi_params;
    }
}
