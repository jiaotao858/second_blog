from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
from comments.forms import CommentForm
import markdown

def index(request):
    post_list = Post.objects.all().order_by('create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request,pk):
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
    return render(request,'blog/detail.html',context={'post':post})

def archives(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})