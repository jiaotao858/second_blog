from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm
import markdown

#   博客首页
def index(request):
    post_list = Post.objects.all()
    return render(request,'blog/index.html',context={'post_list':post_list})

#   博客详情页
def detail(request,pk):
    #   get_object_or_404有就获取，没有就报404
    post = get_object_or_404(Post,pk=pk)
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

#   博客归档
def archives(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    )
    return render(request,'blog/index.html',context={'post_list':post_list})

#   博客分类
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request,'blog/index.html',context={'post_list':post_list})