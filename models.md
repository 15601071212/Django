models.py
```python
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
    owner = models.ForeignKey(User, on_delete = models.CASCADE, db_column='owner', blank=True, null=True,verbose_name="责任人")

    class Meta:
        db_table = 'DevicesPool'
        unique_together = (('device_name', 'domain', 'mgt_address'),)
        verbose_name = "设备资源"  
        verbose_name_plural = "设备资源" 
        
    def __str__(self):
        return "%s::%s" % (self.id, self.device_name)
```
