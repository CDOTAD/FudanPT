# FudanPT
>复旦大学研究生入学考试初试成绩爬取，都怪复旦大学不提供排名

[![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) ![](https://img.shields.io/badge/django-2.0-green.svg) ![](https://img.shields.io/badge/pymysql-0.9.3-green.svg) ![](https://img.shields.io/badge/BeautifulSoup-4.9.3-green.svg)

## Toy Level Website

为了快速上线函数名，文件名都是随便取的，以及没有做任何的安全措施，总之是个玩具级的网站。

隐藏了数据库连接中的用户名和密码。

网站只入库了专业代码为**085211**的专硕和**081201**、**081202**、**081203**以及**083900**的学硕（计算机全部和工研院计算机方向的全部）。

只需要简单将`post_data['nd']`更改为当前年份就可以进行成绩爬取了。
```python
    post_data['nd'] = '2020'
```

## Update

- 2019-3-6

    复旦大学公布了校线：专硕360，学硕340。网站运行半个月后正式关闭。竟然没有被封IP！共统计到492人。其中专硕360及以上共185人，学硕340级以上30人。
  
- 2019-3-xx

    复旦大学计算机学院公布了院线：专硕362，学硕345。

## To Do

- [ ] 爬虫优化？

- [ ] 自动验证码识别


## Nginx + uwsgi + django

- pip install uwsgi 失败

    报错为：
    ```shell
    lto1: fatal error: bytecode stream generated with LTO verstrion 6.0 instead of the expected 4.1
    ```

    使用conda安装：
    ```shell
    conda install -c conda-forge uwsgi python==3.6
    conda install -c conda-forge libiconv
    ```
  
    uwsgi缺少各种libxxx.so.x.x
    参考[uwsgi loading shared libraries:libicui18n.so.58 异常处理](https://blog.csdn.net/MarsYWK/article/details/86704428)
    ```shell
    $ which uwsgi
    /home/username/anaconda3/bin/uwsgi
    
    $ ldd /home/username/anaconda3/bin/uwsgi
    libicui18n.so.58 => not found
    libicuuc.so.58 => not found
    $ find -name libicui18n.so.58 
    /home/username/anaconda3/blablabla/libicui18n.so.58
   
    $ ln -s /home/username/anaconda3/blablabla/libicui18n.so.58 /lib
    $ ln -s /home/username/anaconda3/blablabla/libicui18n.so.58 /lib64
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

- mysql

  ```mysql
    create database student;
  
    create table student(
    id bigint auto_increment primary key ;
    number longtext;
    type int;
    grade int;
    );
    
  ```