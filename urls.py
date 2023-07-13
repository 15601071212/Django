from . import views
from django.urls import re_path as url
from django.urls import path

urlpatterns =[
        url('admin/users/login?next=/share', views.device_share),
        url('share', views.device_share),
        url('link_add/<parm>', views.link_add),
        url('link_add', views.link_add),
        url("index_userinfo", views.index_userinfo, name="index_userinfo"),  
        url("index", views.index, name="index"),  # 首页
        url("deviceinfo", views.deviceinfo, name="deviceinfo"),  # ajax请求表格相关的数据
        url("userinfo", views.userinfo, name="userinfo"),  # ajax请求表格相关的数据
        url("demo", views.pyecharts_demo, name="pyecharts_demo"),
        url("gau", views.gau, name="gau"),
        url('search', views.device_search),
        url('add', views.device_add),
        url('', views.index),
        ]
