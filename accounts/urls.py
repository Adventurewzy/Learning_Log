# WZY
# 干了！
# 2023/07/09 13:45
"""为应用程序accounts定义URL模式"""
from django.urls import path,include
from . import views

app_name = 'accounts'
urlpatterns = [
    #包含默认的身份验证URL
    path('',include('django.contrib.auth.urls')),
    #注册账号页面
    path('register/',views.register,name='register')

]