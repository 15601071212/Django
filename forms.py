from django import forms
from django import forms
from django.forms import widgets

from .models import Devicespool
from .models import Interfaces
from .models import Switchports
from .models import Association

class DevicespoolAdminForm(forms.ModelForm):
    class Meta:
        model = Devicespool
        fields = '__all__'
        widgets = {
            "domain": widgets.TextInput(attrs={"style": "width:40%;","placeholder": "请输入设备域名（当设备与交换机连接时请填写与交换机相同的域名）, 例: UFP_10.229.100.36"}),
            "username": widgets.TextInput(attrs={"placeholder": "请输入登录用户名"}),
            "password": widgets.TextInput(attrs={"placeholder": "请输入登录用户密码"}),
            "device_name": widgets.TextInput(attrs={"placeholder": "请输入设备名称"}),
            "mgt_address": widgets.TextInput(attrs={"placeholder": "请输入设备管理IP"}),
            "priv_cmd": widgets.TextInput(attrs={"placeholder": "请输入提权命令"}),
            "priv_passwd": widgets.TextInput(attrs={"placeholder": "请输入提权密码"}),
        }

class InterfacesAdminForm(forms.ModelForm):
    class Meta:
        model = Interfaces
        fields = '__all__'
        widgets = {
            "device_port": widgets.TextInput(attrs={"style": "width:60%;","placeholder": "当设备型号不是交换机时，请输入设备端口号, 例: 设备端口为 xxvgei-0/1/1/1 或 cgei-0/1/1/1, 测试仪端口为 1/1"}),
            "domain": widgets.TextInput(attrs={"style": "width:60%;","placeholder": "测试仪端口必须填写设备域名, 例: UFP_10.229.100.36"}),
                  }

class SwitchportsAdminForm(forms.ModelForm):
    class Meta:
        model = Switchports
        fields = '__all__'
        widgets = {
            "switch_port": widgets.TextInput(attrs={"style": "width:42%;","placeholder": "当设备型号为交换机时，请输入交换机端口号,例: 物理交换机端口为: xlgei-0/1/0/29 虚拟交换机端口为: vm33mp0ifv1"}),
            "vmname": widgets.TextInput(attrs={"style": "width:42%;","placeholder": '虚拟交换机端口必须填写"vmname",例:虚拟交换机端口为: vm33mp0ifv1 时 "vmname"的值为 vm33-33mp0'}),
        }

class DevicespoolForm(forms.Form):
    device_name = forms.CharField(max_length=25, label='设备名称',error_messages={'required':u'设备名称不能为空'})
    model = forms.CharField(max_length=25, label='设备型号',error_messages={'required':u'设备型号不能为空'})
    mgt_address = forms.GenericIPAddressField(label="管理地址",error_messages={'required':u'管理地址不能为空'})
    username = forms.CharField(max_length=25, label='登录用户',error_messages={'required':u'登录用户不能为空'})
    password = forms.CharField(max_length=25, label='登录密码',error_messages={'required':u'登录密码不能为空'})
