# Nginx Config

nginx.conf 目录：

```shell
cd /etc/nginx
```

将server 配置添加到nginx.conf中的htttp里

```bash

server{
	    listen    1234;
	    server_name 127.0.0.1;
	    charset UTF-8;
	    access_log   /var/log/nginx/mysite_access.log;
	    error_log    /var/log/nginx/mysite_error.log;
	    deny 27.227.92.230;
	   
	    client_max_body_size 75M;
	    
	    location / {
	        include uwsgi_params;
	        uwsgi_pass 127.0.0.1:8000;
		uwsgi_read_timeout 300s;
	    }
	    location /static{
		expires 30d;
		autoindex on;
		add_header Cache-Control private;
		alias /home/zzl/FudanPT/main/static/;
	    }
	}

```
