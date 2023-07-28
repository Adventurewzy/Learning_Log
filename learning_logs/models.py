from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Topic (models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200) #设置主题名不能超过200个字符
    date_added = models.DateTimeField(auto_now_add=True) #记忆创建时间
    #添加新属性public,使登录或未登录的用户看到其他用户的公开主题
    public = models.BooleanField(default=False)
    #使主题与用户绑定,用户被删除时其中的主题也会被删除
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text

class Entry (models.Model):
    """学到的有关某个主题的具体知识(创建条目)"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    #ForeignKey(Topic将每个条目关联到特定的主题,  实参on_delete=models.CASCADE,使删除主题时,同时删除相关联的条目
    text = models.TextField() #条目的字数不受限制
    date_added = models.DateTimeField(auto_now_add=True)
    #按创建顺序呈现条目,并在每个条目旁边放置时间戳.

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回一个表示条目的简单字符串"""
        if len(self.text) <= 50:
            return self.text
        else:
            return f"{self.text[:50]}..." #让__str__方法只返回text的前50个字符
