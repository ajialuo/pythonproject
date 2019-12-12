from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Article, Category, Banner, Tag, Link



def global_variable(request):
    allcategory = Category.objects.all()
    remen = Article.objects.filter(tui__id=1)[:6]
    tags = Tag.objects.all()
    return locals()

# 首页
def index(request):
    banner = Banner.objects.filter(is_active=True)[0:4] # 查询所有幻灯图数据，并进行切片
    tui = Article.objects.filter(tui__id=1)[:3]  # 查询推荐位ID为1的文章
    allarticle = Article.objects.all().order_by('-id')[0:10]
    hot = Article.objects.all().order_by('views')[:10]  # 通过浏览数进行排序
    link = Link.objects.all()
    return render(request,'index.html',locals())

# 列表页
def list(request,lid):
    list = Article.objects.filter(category_id=lid)    # 获取通过URL传进来的lid,然后筛选出对应文章
    cname = Category.objects.get(id=lid)    # 获取当前文章的栏目名
    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list,5)   # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)    # 如果用户输入的页码不是整数时，显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request,'list.html',locals())

#内容页
def show(request,sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    hot = Article.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()
    next_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    show.views = show.views + 1
    show.save()
    return render(request,'show.html',locals())

#标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)   # 通过文章标签进行查询文章
    tname = Tag.objects.get(name=tag)   # 获取当前搜索的标签名
    page = request.GET.get('page')
    paginator = Paginator(list,5)

    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)    # 如果用户输入的页码不是整数时，显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request,'tags.html',locals())

# 搜索页
def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配
    page = request.GET.get('page')
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())
# 关于我们
def about(request):
    return render(request, 'page.html', locals())
