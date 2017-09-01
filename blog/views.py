from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm
import markdown
from django.views.generic import ListView,DetailView  #通用视图类

#   博客首页方法普通方法
# def index(request):
#     post_list = Post.objects.all()
#     return render(request,'blog/index.html',context={'post_list':post_list})

#   博客首页方法二：通用视图类
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #指定paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 2

    def get_context_data(self, **kwargs):

        #首先获取父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        #父类生成的字典中已有paginator、page_obj、is_paginated
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator,page,is_paginated)

  # 博客详情页：普通方法
def detail(request,pk):
    #   get_object_or_404有就获取，没有就报404
    post = get_object_or_404(Post,pk=pk)

    #阅读量+1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    #   获取这篇 post 下全部评论
    comment_list = post.comment_set.all()

    #   将文章、表单、以及文章下的评论列表作为模板变量传递给 detail.html，以便渲染数据
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
                }
    return render(request,'blog/detail.html',context=context)
# 博客详情页：通用视图类


#   博客归档一：普通方法
# def archives(request,year,month):
#     post_list = Post.objects.filter(create_time__year=year,
#                                     create_time__month=month
#                                     )
#     return render(request,'blog/index.html',context={'post_list':post_list})


#   博客归档二：通用视图类
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year =self.kwargs.get('year')
        month =self.kwargs.get('month')
        return super(ArchivesView,self).get_queryset().filter(create_time__year=year,
                                                              create_time__month=month,
                                                              )
#   博客分类方法一：普通方法
# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request,'blog/index.html',context={'post_list':post_list})

#   博客分类方法二：通用视图类
class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)
