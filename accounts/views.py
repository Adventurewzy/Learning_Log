from django import forms
from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
class CustomUserCreationForm(UserCreationForm):
    """自定义django提供的用户注册表单,汉化注册表单中的提示语"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = '请输入您的自定义用户名'
        self.fields['username'].help_text = '用户名仅限字母、数字和@/./+/-/_。用户名不得超过150个字符.'
        self.fields['password1'].label = '请输入您的密码'
        self.fields['password1'].help_text = '密码必须包含8个字符,且不能全是数字.'
        self.fields['password2'].label = '请输入您的密码'
        self.fields['password2'].help_text = '为了确认请再次输入您的密码.'


def register(request):
    """注册新用户"""
    if request.method != 'POST':
        #显示空的表单
        form = CustomUserCreationForm()
    else:
        #处理填写好的表单
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #使完成注册的用户自动登陆,并回到主页
            login(request,new_user)
            return redirect('learning_logs:index')

    #显示空表单,或指出表单无效
    context = {'form':form}
    return render(request,'registration/register.html',context)
