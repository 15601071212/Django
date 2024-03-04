# 用Django搭建Web应用第一章
## 安装
### 1. 安装Django
> 检查当前Python版本
```bash
root@zdh-web-00:~# python3
Python 3.8.10 (default, Nov 22 2023, 10:22:35) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
最新版本Python下载路径：

https://www.python.org/downloads/

用pip安装Django并指定版本号: pip install "Django==4.1.*"

检查当前Django版本
```bash
root@zdh-web-00:~# python3
Python 3.8.10 (default, Nov 22 2023, 10:22:35) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.get_version()
'4.1.5'
>>> 
```
Django安装手册：

https://docs.djangoproject.com/en/3.0/topics/install/

### 2. 创建项目(project)
用命令行django-admin startproject mysite

创建一个名为blog的应用，生成的mysite文件夹及相关的文件如下所示：

```bash
root@zdh-web-00:/var/www# django-admin startproject mysite
root@zdh-web-00:/var/www# ls -al | grep mysite
drwxr-xr-x  3 root root      4096 Mar  4 10:56 mysite
root@zdh-web-00:/var/www# cd mysite
root@zdh-web-00:/var/www/mysite# tree
.
├── manage.py
└── mysite
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 6 files
root@zdh-web-00:/var/www/mysite#
```
> 本地数据库迁移
```bash
root@zdh-web-00:/var/www/mysite# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
root@zdh-web-00:/var/www/mysite# 
```
> 运行开发服务器
```bash
root@zdh-web-00:/var/www/mysite# python3 manage.py runserver 0.0.0.0:8888
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 04, 2024 - 03:01:43
Django version 4.1.5, using settings 'mysite.settings'
Starting development server at http://0.0.0.0:8888/
Quit the server with CONTROL-C
```
如果需要远程访问开发服务器默认Web页面，需要在settings.py文件中把下面这行：

ALLOWED_HOSTS = []

改为如下所示：

ALLOWED_HOSTS = ['*']

表示允许所有的主机远程访问开发服务器默认Web页面http://10.229.191.63:8888/

> settings.py文件路径如下：
```bash
root@zdh-web-00:/var/www/mysite/mysite# pwd
/var/www/mysite/mysite
root@zdh-web-00:/var/www/mysite/mysite# ls -al
total 28
drwxr-xr-x 3 root root 4096 Mar  4 11:06 .
drwxr-xr-x 3 root root 4096 Mar  4 10:59 ..
-rw-r--r-- 1 root root  389 Mar  4 10:56 asgi.py
-rw-r--r-- 1 root root    0 Mar  4 10:56 __init__.py
drwxr-xr-x 2 root root 4096 Mar  4 11:06 __pycache__
-rw-r--r-- 1 root root 3224 Mar  4 11:06 settings.py
-rw-r--r-- 1 root root  748 Mar  4 10:56 urls.py
-rw-r--r-- 1 root root  389 Mar  4 10:56 wsgi.py
root@zdh-web-00:/var/www/mysite/mysite#
```
> 打开浏览器输入以下网址可以成功远程访问开发服务器默认Web页面：

> http://172.232.187.216:8888/

> 如果从本地访问开发服务器默认Web页面http://127.0.0.1:8000/

> 则不需要python3 manage.py runserver添加参数0.0.0.0：8888和修改settings.py文件
```bash
root@zdh-web-00:/var/www/mysite# python3 manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 04, 2024 - 03:16:58
Django version 4.1.5, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
> 打开浏览器输入以下网址可以成功远程访问开发服务器默认Web页面如上图所示：

> http://127.0.0.1:8000/

> 每一次HTTP请求都会有Log记录在控制台(console)上，如下所示：
```bash
root@zdh-web-00:/var/www/mysite# python3 manage.py runserver 0.0.0.0:8888
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 04, 2024 - 03:23:39
Django version 4.1.5, using settings 'mysite.settings'
Starting development server at http://0.0.0.0:8888/
Quit the server with CONTROL-C.
[04/Mar/2024 03:23:48] "GET / HTTP/1.1" 200 10681
```
> 以下链接是如何将Django部署在Apache等各种实际环境中Web服务器上的文档：

> https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/

### 3. 创建应用(application)
> 用命令行python3 manage.py startapp blog创建一个名为blog的应用，生成的blog文件夹及相关文件如下所示：
```bash
root@zdh-web-00:/var/www/mysite# python3 manage.py startapp blog
root@zdh-web-00:/var/www/mysite# ls -al | grep blog
drwxr-xr-x  3 root root   4096 Mar  4 11:27 blog
root@zdh-web-00:/var/www/mysite# tree
.
├── blog
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── manage.py
└── mysite
    ├── asgi.py
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   ├── settings.cpython-38.pyc
    │   ├── urls.cpython-38.pyc
    │   └── wsgi.cpython-38.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

4 directories, 18 files
root@zdh-web-00:/var/www/mysite# 
```

