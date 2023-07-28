from django.contrib import admin

# Register your models here.
from .models import Topic,Entry
#导入注册模型,models前面的‘.’让Django在admin.py所在的目录中查找models.py

admin.site.register(Topic)  #admin.site.register()让Django通过管理网站管理模型.
admin.site.register(Entry)