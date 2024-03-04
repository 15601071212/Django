# 用Django搭建Web应用 第二章
## 设计应用的数据架构(data schema)、创建数据模型的管理网站并且添加数据模型到管理网站
### 1. 设计应用的数据架构(data schema)
> 以设计MariaDB数据库中的设备数据表Devicespool为例，在项目mysite的应用blog的文件夹下在models.py文件中添加名为Devicespool的类(class)如下所示：
```bash
root@localhost:/var/www/LRM/lrm# pwd
/var/www/LRM/lrm
root@localhost:/var/www/LRM/lrm# more models.py
```
```python
from django.db import models

MODEL_CHOICES = (
            ('ssp', 'zxrufp::ssp'),
            ('ufp', 'zxrufp::ufp'),
            ('ufp-070', 'zxrufp::ufp-070'),
            ('ufp-59x', 'zxrufp::ufp-59x'),
            ('ufp-61', 'zxrufp::ufp-61'),
    )
STATUS_CHOICES = (
        ('IDLE', 'IDLE'),
        ('INUSE', 'INUSE'),
        ('NotAccess', 'NotAccess'),
    )
PORT_RATE_CHOICES = (
        ('1G', '1G'),
        ('10G', '10G'),
        ('25G', '25G'),
        ('40G', '40G'),
        ('50G', '50G'),
        ('100G', '100G'),
        ('200G', '200G'),
        ('400G', '400G'),
    )       
MGT_PORT_CHOICES = (
        ('22', 'SSH:22'),
        ('23', 'Telnet:23'),
        ('3082', 'Telnet:3082'),
        ('3083', 'Telnet:3083'),
    )   
CONNECT_CHOICES = (
        ('ssh', 'SSH'),
        ('telnet', 'Telnet'),
    )       
class Devicespool(models.Model):
    testbedid = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备型号",choices=MODEL_CHOICES,help_text='参数文件中"model"的值')
    device_name = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备名称",help_text='参数文件中"device_name"的值')
    domain = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备域名",help_text='参数文件中"domain"的值')
    status = models.CharField(max_length=50, blank=False, null=True,verbose_name="设备状态",choices=STATUS_CHOICES,default='IDLE')
    user = models.CharField(max_length=50, blank=True, null=True,verbose_name="执行机用户名")
    connect = models.CharField(max_length=50, blank=False, null=True,verbose_name="连接方式",choices=CONNECT_CHOICES,default='ssh',help_text='参数文件中"fv-connect"的值')
    mgt_address = models.GenericIPAddressField(blank=False, null=True,verbose_name="连接地址",help_text='参数文件中"fv-mgt_addr"的值')
    mgt_port = models.CharField(max_length=50, blank=False, null=True,verbose_name="连接端口",choices=MGT_PORT_CHOICES,default='22',help_text='参数文件中"fv-mgt_port"的值')
    com_address = models.CharField(max_length=50, blank=True, null=True)
    com_port = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=False, null=True,verbose_name="登录用户名",help_text='参数文件中"fv-username"的值')
    password = models.CharField(max_length=50, blank=False, null=True,verbose_name="登录密码",help_text='参数文件中"fv-password"的值')
    ports_num_total = models.IntegerField(blank=True, null=True)
    device_tag = models.CharField(max_length=250, blank=True, null=True)
    board_tag = models.CharField(max_length=250, blank=True, null=True)
    board_type = models.CharField(max_length=250, blank=True, null=True)
    slot = models.CharField(max_length=100, blank=True, null=True)
    board_num = models.IntegerField(blank=True, null=True)
    priv_cmd = models.CharField(max_length=50, blank=False, null=True,verbose_name="提权命令",default='enable',help_text='参数文件中"fv-privileged_command"的值')
    priv_passwd = models.CharField(max_length=50, blank=False, null=True,verbose_name="提权密码",default= 'zxr10',help_text='参数文件中"fv-privileged_password"的值')
    maintain = models.CharField(max_length=50, blank=True, null=True,default='9999')
    rfassets = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=False, null=True,verbose_name="创建时间") 
    updated_at = models.DateTimeField(auto_now=True,blank=False, null=True,verbose_name="更新时间")

    class Meta:
        db_table = 'DevicesPool'
        unique_together = (('device_name', 'domain', 'mgt_address'),)
        verbose_name = "设备资源"  
        verbose_name_plural = "设备资源" 
        
    def __str__(self):
        return "%s::%s" % (self.id, self.device_name)
```
> 在models.py文件中定义了一个应用的数据模型之后，用下面的命令将数据模型迁移到数据库：
python3 manage.py makemigrations lrm(生成用于迁移的数据库shell命令行)
python3 manage.py migrate(连接数据库执行数据库迁移命令)：
```bash
root@localhost:/var/www/LRM# python3 manage.py makemigrations lrm
Migrations for 'lrm':
  lrm/migrations/0001_initial.py
    - Create model Devicespool
root@localhost:/var/www/LRM# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, lrm, sessions
Running migrations:
  Applying lrm.0001_initial... OK
root@localhost:/var/www/LRM# 
```
> 用下面的命令通过应用名和序号查询对应的MySQL命令：
```bash
root@localhost:/var/www/LRM# python3 manage.py sqlmigrate lrm 0001
BEGIN;
--
-- Create model Devicespool
--
CREATE TABLE "DevicesPool" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "testbedid" integer NULL, "model" varchar(50) NULL, "device_name" varchar(50) NULL, "domain" varchar(50) NULL, "status" varchar(50) NULL, "user" varchar(50) NULL, "connect" varchar(50) NULL, "mgt_address" char(39) NULL, "mgt_port" varchar(50) NULL, "com_address" varchar(50) NULL, "com_port" varchar(50) NULL, "username" varchar(50) NULL, "password" varchar(50) NULL, "ports_num_total" integer NULL, "device_tag" varchar(250) NULL, "board_tag" varchar(250) NULL, "board_type" varchar(250) NULL, "slot" varchar(100) NULL, "board_num" integer NULL, "priv_cmd" varchar(50) NULL, "priv_passwd" varchar(50) NULL, "maintain" varchar(50) NULL, "rfassets" varchar(50) NULL, "created_at" datetime NULL, "updated_at" datetime NULL);
CREATE UNIQUE INDEX "DevicesPool_device_name_domain_mgt_address_941c95bf_uniq" ON "DevicesPool" ("device_name", "domain", "mgt_address");
COMMIT;
root@localhost:/var/www/LRM# 
```
> 默认生成的在Django自带的数据库中数据表名称为用下划线连接的应用名称和模型中类(class)名称的小写形式：blog_devicespool，可以在Meta类(class)中自定义数据库中数据表的名称db_table = 'Devicespool'


```python
    class Meta:
        #managed = False
        db_table = 'Devicespool'
        unique_together = (('device_name', 'domain', 'mgt_address'),)
        verbose_name = "设备资源"  
        verbose_name_plural = "设备资源"
```
> 注释掉Meta类(class)中managed = False参数上述迁移命令python3 manage.py makemigrations blog和python3 manage.py migrate才能生效
```bash
root@localhost:/var/www/LRM# python3 manage.py makemigrations lrm
Migrations for 'lrm':
  lrm/migrations/0002_alter_devicespool_table.py
    - Rename table for devicespool to Devicespool
root@localhost:/var/www/LRM# python3 manage.py sqlmigrate lrm 0002
BEGIN;
--
-- Rename table for devicespool to Devicespool
--
-- (no-op)
COMMIT;
root@localhost:/var/www/LRM# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, lrm, sessions
Running migrations:
  Applying lrm.0002_alter_devicespool_table... OK
root@localhost:/var/www/LRM# 
```
> 注：如果连接的数据库中已经有数据表，可以用 python3 manage.py inspectdb命令将数据表的格式导出到一个数据模型文件中，注释掉Meta类(class)中managed = False参数后，Django就可以对已有的数据表进行创建、修改和删除操作。
```bash
root@localhost:/var/www/LRM# python3 manage.py inspectdb > models.py
root@localhost:/var/www/LRM# more models.py
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Devicespool(models.Model):
    testbedid = models.IntegerField(blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    device_name = models.CharField(max_length=50, blank=True, null=True)
    domain = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    connect = models.CharField(max_length=50, blank=True, null=True)
    mgt_address = models.CharField(max_length=39, blank=True, null=True)
    mgt_port = models.CharField(max_length=50, blank=True, null=True)
    com_address = models.CharField(max_length=50, blank=True, null=True)
    com_port = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    ports_num_total = models.IntegerField(blank=True, null=True)
    device_tag = models.CharField(max_length=250, blank=True, null=True)
    board_tag = models.CharField(max_length=250, blank=True, null=True)
    board_type = models.CharField(max_length=250, blank=True, null=True)
    slot = models.CharField(max_length=100, blank=True, null=True)
    board_num = models.IntegerField(blank=True, null=True)
    priv_cmd = models.CharField(max_length=50, blank=True, null=True)
    priv_passwd = models.CharField(max_length=50, blank=True, null=True)
    maintain = models.CharField(max_length=50, blank=True, null=True)
    rfassets = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DevicesPool'
        unique_together = (('device_name', 'domain', 'mgt_address'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
root@localhost:/var/www/LRM# 
```
### 2. 创建数据模型的管理网站
> 执行命令python3 manage.py createsuperuser创建管理员账号admin和密码如下所示：
```bash
root@localhost:/var/www/LRM# python3 manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: admin@skynet.com
Password: 
Password (again): 
Superuser created successfully.
root@localhost:/var/www/LRM#
```
创建管理员账号后访问网址 http://139.144.210.48:8888/admin 可以看到下面的登录页面：
![image](https://github.com/15601071212/Django/assets/17488098/0540fc6c-3a8b-4071-a25e-8c75efde3485)

> 注1：编辑/var/www/LRM/LRM/settings.py配置文件，将LANGUAGE_CODE设置为 'zh-hans'可以，可以在管理页面中显示中文
```python
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
#LANGUAGE_CODE = 'en-us'
```
![image](https://github.com/15601071212/Django/assets/17488098/b0bed307-a031-40ee-b22b-fc363497731f)

> 注2：编辑/var/www/mysite/blog/apps.py设置VERBOSE_APP_NAME = "设备资源管理"，可以在管理页面中设置应用(APP)的中文名称
```python
from django.apps import AppConfig

VERBOSE_APP_NAME = "设备资源管理"

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = VERBOSE_APP_NAME
```
![image](https://github.com/15601071212/Django/assets/17488098/2470612b-04dc-4f0f-b570-856116aef457)

> 注3：编辑/var/www/mysite/blog/admin.py添加如下配置自定义Django项目管理网站的中文名称与标题：
```python
from django.contrib import admin

admin.site.site_header="自动化测试中台管理系统"

admin.site.site_title="自动化测试中台资源库"

admin.site.index_title="自动化测试中台资源库"
```
> 上述设置生效后，用admin账号和密码登录Django项目管理网站页面后可以看到网站名称和标题已经改为自定义的中文名称：
http://10.229.191.63:8888/admin
![image](https://github.com/15601071212/Django/assets/17488098/9189bc96-b66f-48df-bbee-95b5a22335a6)

### 3. 添加数据模型到管理网站
> 编辑/var/www/LRM/lrm/models.py文件中数据表Devicespool的数据模型类Devicespool中的Meta类下的verbose_name和verbose_name_plural参数可以定义数据表在Django管理页面中的中文名称：
```python
class Devicespool(models.Model):
    class Meta:
        verbose_name = "设备资源"  
        verbose_name_plural = "设备资源"
```
修改后管理网站页面显示如下图所示：
![image](https://github.com/15601071212/Django/assets/17488098/1b55bcbf-d3a9-4b63-b026-92fe8fada02e)

> 编辑/var/www/LRM/lrm/admin.py文件，添加如下所示的代码可以在Django管理页面上显示数据模型(model)类Devicespool对应的数据库中数据表Devicespool的数据字段显示列表(list_display)、过滤器(list_filter)和搜索框(search_fields)：
```python
from django.contrib import admin

from .models import Devicespool

@admin.register(Devicespool)

class LrmDeviceAdmin(admin.ModelAdmin):
    model = Devicespool
    admin_order =1
    list_display = ("device_name", "model", "domain","status", "mgt_address", "mgt_port")
    list_filter = ("model", "status")
    search_fields = ("device_name", "model", "domain", "status", "mgt_address")

```
修改后管理网站页面显示如下图所示：
![image](https://github.com/15601071212/Django/assets/17488098/73956b60-baf8-4707-8b8e-0321a89f04ff)
