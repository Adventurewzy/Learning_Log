# WZY
# 干了！
# 2023/07/07 12:35
from django import forms
from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text','public']
        labels = {'text' : '' }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text' : ''}
        #使文本框的宽度增加到80
        widgets = {'text' : forms.Textarea(attrs={'cols':80})}
