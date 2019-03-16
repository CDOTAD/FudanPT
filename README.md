# FudanPT
>复旦大学研究生入学考试初试成绩爬取，都怪复旦大学不提供排名

![](https://img.shields.io/badge/license-MIT-blue.svg) ![](https://img.shields.io/badge/django-2.0-green.svg) ![](https://img.shields.io/badge/pymysql-0.9.3-green.svg) ![](https://img.shields.io/badge/BeautifulSoup-4.6.0-green.svg)

## Toy Level Website

为了快速上线函数名，文件名都是随便取的，以及没有做任何的安全措施，总之是个玩具级的网站。

隐藏了数据库连接中的用户名和密码。

网站只入库了专业代码为**085211**的专硕和**081201**、**081202**、**081203**以及**083900**的学硕（计算机全部和工研院计算机方向的全部）。

## Update

- 2019-3-6

    复旦大学公布了校线：专硕360，学硕340。网站运行半个月后正式关闭。竟然没有被封IP！共统计到492人。其中专硕360及以上共185人，学硕340级以上30人。
  
- 2019-3-xx

    复旦大学计算机许愿公布了院线：专硕362，学硕345。


## Nginx + uwsgi + django

- pip install uswgi 失败

    报错为：
    ```shell
    lto1: fatal error: bytecode stream generated with LTO verstrion 6.0 instead of the expected 4.1
    ```

    使用conda安装：
    ```shell
    conda install -c conda-forge uwsgi
    conda install -c conda-forge libiconv
    ```

- 通过[.ini](mysite_uwsgi.ini)文件配置uwsgi并启动。

    - uwsgi 启动停止重启

        - 启动：
            ```shell
            uwsgi --ini xxx.ini
            ```
        
        - 重启:
            ```shell
            uwsgi --reload xxx.pid
            ```
        
        - 停止：
            ```shell
            uwsgi --stop xxx.pid
            ```
        .pid 文件需要在uwsgi的配置文件uwsgi.ini文件中设置
        ```shell
        pidfile=%(chdir)/uwsgi/uwsgi.pid
        ```

        - 强制关闭：
            ```shell
            sudo killall -9 uwsgi
            ```

- nginx [配置](nginx_conf)

    - nginx 启动：
        ```shell
        sudo nginx
        ```
    - nginx 重启:
        ```shell
        sudo nginx -s reload
        ```
    - nginx 关闭:
        ```shell
        sudo nginx -s stop
        ```

