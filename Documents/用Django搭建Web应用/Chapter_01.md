# 用Django搭建Web应用 第一章
## 安装Django并创建项目（project）与应用（app）
### 1. 安装Django
> 检查当前Python版本
```bash
root@localhost:~# python3
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```
最新版本Python下载路径：

https://www.python.org/downloads/

用pip安装Django并指定版本号: pip install "Django==4.1.*"

检查当前Django版本
```bash
root@localhost:~# python3
Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> django.get_version()
'4.2.7'
>>> 
```
Django安装手册：

https://docs.djangoproject.com/en/3.0/topics/install/

### 2. 创建项目(project)
用命令行django-admin startproject mysite

创建一个名为blog的应用，生成的mysite文件夹及相关的文件如下所示：

```bash
root@localhost:/var/www# django-admin startproject mysite
root@localhost:/var/www# ls -al | grep LRM
drwxr-xr-x  3 root root 4096 Mar  4 21:04 LRM
root@localhost:/var/www# cd LRM
root@localhost:/var/www/LRM# tree
.
├── LRM
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

1 directory, 6 files
root@localhost:/var/www/LRM# 
```
> 本地数据库迁移
```bash
root@localhost:/var/www/LRM# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
root@localhost:/var/www/LRM# 
```
> 运行开发服务器
```bash
root@localhost:/var/www/LRM# python3 manage.py runserver 0.0.0.0:8888
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 04, 2024 - 13:17:29
Django version 4.2.7, using settings 'LRM.settings'
Starting development server at http://0.0.0.0:8888/
Quit the server with CONTROL-C.
```
如果需要远程访问开发服务器默认Web页面，需要在settings.py文件中把下面这行：

ALLOWED_HOSTS = []

改为如下所示：

ALLOWED_HOSTS = ['*']

表示允许所有的主机远程访问开发服务器默认Web页面http://139.144.210.48:8888/

> settings.py文件路径如下：
```bash
root@localhost:/var/www/LRM/LRM# pwd
/var/www/LRM/LRM
root@localhost:/var/www/LRM/LRM# ls -al
total 28
drwxr-xr-x 3 root root 4096 Mar  4 21:15 .
drwxr-xr-x 3 root root 4096 Mar  4 21:15 ..
-rw-r--r-- 1 root root  383 Mar  4 21:04 asgi.py
-rw-r--r-- 1 root root    0 Mar  4 21:04 __init__.py
drwxr-xr-x 2 root root 4096 Mar  4 21:20 __pycache__
-rw-r--r-- 1 root root 3215 Mar  4 21:20 settings.py
-rw-r--r-- 1 root root  759 Mar  4 21:04 urls.py
-rw-r--r-- 1 root root  383 Mar  4 21:04 wsgi.py
root@localhost:/var/www/LRM/LRM# 
```
> 打开浏览器输入以下网址可以成功远程访问开发服务器默认Web页面：

http://139.144.210.48:8888/
![image](https://github.com/15601071212/Django/assets/17488098/f4177b09-5e6c-4ed0-87a2-56633b567863)

> 如果从本地访问开发服务器默认Web页面http://127.0.0.1:8000/

> 则不需要python3 manage.py runserver添加参数0.0.0.0：8888和修改settings.py文件
```bash
root@localhost:/var/www/LRM# python3 manage.py runserver
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
root@localhost:/var/www/LRM# python3 manage.py runserver 0.0.0.0:8888
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 04, 2024 - 13:20:21
Django version 4.2.7, using settings 'LRM.settings'
Starting development server at http://0.0.0.0:8888/
Quit the server with CONTROL-C.

[04/Mar/2024 13:20:26] "GET / HTTP/1.1" 200 10664
```
> 以下链接是如何将Django部署在Apache等各种实际环境中Web服务器上的文档：

> https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/

### 3. 创建应用(application)
> 用命令行python3 manage.py startapp lrm创建一个名为lrm的应用，生成的lrm文件夹及相关文件如下所示：
```bash
root@localhost:/var/www/LRM# python3 manage.py startapp lrm
root@localhost:/var/www/LRM# ls -al | grep lrm
drwxr-xr-x 3 root root   4096 Mar  4 21:26 lrm
root@localhost:/var/www/LRM# tree
.
├── db.sqlite3
├── lrm
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── LRM
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── settings.cpython-310.pyc
│   │   ├── urls.cpython-310.pyc
│   │   └── wsgi.cpython-310.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

4 directories, 18 files
root@localhost:/var/www/LRM#  
```
> 在:/var/www/LRM/LRM路径下的settings.py文件中添加名称为lrm的应用（APP）如下所示：
```python
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lrm',
]
```
