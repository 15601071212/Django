# 用Django搭建Web应用 第二章
## 设计应用的数据架构(data schema)、创建数据模型的管理网站并且添加数据模型到管理网站
### 1. 设计应用的数据架构(data schema)
> 以设计MariaDB数据库中的设备数据表Devicespool为例，在项目mysite的应用blog的文件夹下在models.py文件中添加名为Devicespool的类(class)如下所示：
```bash
root@zdh-web-00:/var/www/mysite/blog# pwd
/var/www/mysite/blog
root@zdh-web-00:/var/www/mysite/blog# more models.py
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
python3 manage.py makemigrations blog(生成用于迁移的数据库shell命令行)
python3 manage.py migrate(连接数据库执行数据库迁移命令)：
```bash
root@zdh-web-00:/var/www/mysite# python3 manage.py makemigrations blog
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Devicespool
root@zdh-web-00:/var/www/mysite# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0001_initial... OK
root@zdh-web-00:/var/www/mysite# 
```
> 用下面的命令通过应用名和序号查询对应的MySQL命令：
```bash
root@zdh-web-00:/var/www/mysite# python3 manage.py sqlmigrate blog 0001
BEGIN;
--
-- Create model Devicespool
--
CREATE TABLE "DevicesPool" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "testbedid" integer NULL, "model" varchar(50) NULL, "device_name" varchar(50) NULL, "domain" varchar(50) NULL, "status" varchar(50) NULL, "user" varchar(50) NULL, "connect" varchar(50) NULL, "mgt_address" char(39) NULL, "mgt_port" varchar(50) NULL, "com_address" varchar(50) NULL, "com_port" varchar(50) NULL, "username" varchar(50) NULL, "password" varchar(50) NULL, "ports_num_total" integer NULL, "device_tag" varchar(250) NULL, "board_tag" varchar(250) NULL, "board_type" varchar(250) NULL, "slot" varchar(100) NULL, "board_num" integer NULL, "priv_cmd" varchar(50) NULL, "priv_passwd" varchar(50) NULL, "maintain" varchar(50) NULL, "rfassets" varchar(50) NULL, "created_at" datetime NULL, "updated_at" datetime NULL);
CREATE UNIQUE INDEX "DevicesPool_device_name_domain_mgt_address_941c95bf_uniq" ON "DevicesPool" ("device_name", "domain", "mgt_address");
COMMIT;
root@zdh-web-00:/var/www/mysite#
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
root@zdh-web-00:/var/www/mysite# python3 manage.py makemigrations blog
Migrations for 'blog':
  blog/migrations/0002_alter_devicespool_table.py
    - Rename table for devicespool to Devicespool
root@zdh-web-00:/var/www/mysite# python3 manage.py sqlmigrate blog 0002
BEGIN;
--
-- Rename table for devicespool to Devicespool
--
-- (no-op)
COMMIT;
root@zdh-web-00:/var/www/mysite# python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0002_alter_devicespool_table... OK
root@zdh-web-00:/var/www/mysite#
```
