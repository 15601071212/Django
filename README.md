# Django 项目开发示例
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
root@zdh-web-00:~# django-admin startproject mysite

root@zdh-web-00:~# ls -al | grep mysite

drwxr-xr-x  3 root      root         4096 Dec 28 16:31 mysite

root@zdh-web-00:~# cd mysite

root@zdh-web-00:~/mysite# tree

.

├── db.sqlite3

├── manage.py

└── mysite

├── asgi.py

├── __init__.py

├── __pycache__

│   ├── __init__.cpython-38.pyc

│   ├── settings.cpython-38.pyc

│   └── urls.cpython-38.pyc

├── settings.py

├── urls.py

└── wsgi.py

2 directories, 10 files

root@zdh-web-00:~/mysite#
```
