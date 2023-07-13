### **LRM/lrm/models.py**
```python
from django.apps import AppConfig

VERBOSE_APP_NAME = "设备资源管理"

class LrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lrm'
    verbose_name = VERBOSE_APP_NAME

```
