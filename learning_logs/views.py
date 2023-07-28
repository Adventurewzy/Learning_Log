from django.shortcuts import render,redirect
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required  #django自带的限制器login_required可以限制未登录的用户访问topic
from django.http import Http404
# Create your views here.

def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')

def topics(request):
    """显示所有的主题"""
    if request.user.is_authenticated:
        #如果用户已登录,就获取其所有主题,以及其他用户的所有公开主题
        topics = Topic.objects.filter(owner=request.user).order_by('date_added')
        #获取不归当前用户所有的其他公开主题
        public_topics = Topic.objects.filter(public=True).exclude(owner=request.user).order_by('date_added')
    else:
        #用户未通过身份验证
        topics = None
        public_topics = Topic.objects.filter(public=True).order_by('date_added')

    context = {'topics' : topics,'public_topics' : public_topics}
    return render(request, 'learning_logs/topics.html', context)


def check_topic_owner(topic,request):
    """核实执行操作的用户是否为该主题的关联用户"""
    if topic.owner != request.user:
        raise Http404



def topic(request,topic_id):
    """显示单个主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)
    #仅当该主题归该用户所用时,才是显示链接new_entry和edit_entry.
    is_owner = False
    if request.user == topic.owner:
        is_owner = True
    #如果该主题归他人所有,且不是公开的,显示错误页面.
    if (topic.owner != request.user) and (not topic.public):
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic , 'entries': entries,'is_owner' : is_owner}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据: 创建一个新表单(如果用户的请求不是post)
        form = TopicForm()
    else:
        #请求为post的数据:对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            #检查用户提交的信息是否有效
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            #保存数据后,使用redirect()将用户的浏览器重新定向‘topics’界面
            return redirect('learning_logs:topics')

    context = {'form': form }
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic,request)
    if request.method != 'POST':
        #未提交数据: 创建一个新表单(如果用户的请求不是post)
        form = EntryForm()
    else:
        #如果是请求为post的数据:对数据进行处理
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            #让Django创建一个新条目并赋值给new_entry,但不保存到数据库中
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)

    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_topic(request,topic_id):
    """编辑既有主题名称"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic,request)

    if request.method != 'POST':
        #初次请求时,使用当前主题填充表单
        form = TopicForm(instance=topic)
    else:
        #post请求提交数据:对数据进行处理
        form = TopicForm(instance=topic,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id = topic.id)

    context = {'topic': topic,'form' : form}
    return render(request,'learning_logs/edit_topic.html',context)

@login_required
def edit_entry(request,entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(topic,request)

    if request.method != 'POST':
        #初次请求,使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        #post请求提交数据: 对数据进行处理
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id = topic.id)

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)

@login_required
def delete_topic(request,topic_id):
    """删除既有主题"""
    try:
        topic = Topic.objects.get(id=topic_id, owner=request.user)
    except Topic.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')

    context = {'topic' : topic}
    return render(request,'learning_logs/delete_topic.html',context)

@login_required
def delete_entry(request,entry_id):
    """删除既有条目"""
    try:
        entry = Entry.objects.get(id=entry_id)
        topic = entry.topic
        topic.owner = request.user
    except Topic.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic',topic_id=topic.id)

    context = {'topic':topic,'entry':entry}
    return render(request,'learning_logs/delete_entry.html',context)
