from django.apps import AppConfig

VERBOSE_APP_NAME = "测试脚本管理"

class SrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'srm'
    verbose_name = VERBOSE_APP_NAME
