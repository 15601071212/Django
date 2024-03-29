### 步骤1: 环境搭建
- **1. 安装Python和Django:** 确保你的开发环境中已经安装了Python和Django。如果还没有安装，你可以访问Python官网和Django官网获取安装指南。

- **2. 创建Django项目:* 打开终端或命令提示符，运行以下命令创建一个新的Django项目。

```shell
django-admin startproject question_db
```

> 进入项目目录：

```shell
cd question_db
```

- **3. 安装Django REST framework:** 使用pip安装Django REST framework。

```shell
pip install djangorestframework
```

- **4.添加'app'和'rest_framework'到你的项目设置:** 打开question_db/settings.py，在INSTALLED_APPS中添加创建的app（稍后创建）和rest_framework。
