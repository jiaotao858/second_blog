from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request,post_pk):
    #   get_object_or_404存在即获取，不存在则返回404
    post = get_object_or_404(Post,pk=post_pk)

    #   HTTP请求有get和post两种，一般用户通过表单提交数据都是通过post请求，
    #   因此我们只有当用户请求为post时才需要处理表单数据
    if request.method == 'POST':
        #   用户提交的数据存储在request.PSOT中，这是一个类字典对象。
        #   我们利用这些数据构造CommentForm的实例,这样Django表单就生成了。
        form = CommentForm(request.POST)

        #   调用form.is_valid()方法，Django自动检查表单的数据是否符合相求
        if form.is_valid():
            #   检查到数据是合法的，调用表单的save方法保存数据到数据库中，
            #   commint=False的作用是仅仅利用表单的数据生成Comment的模型类的实例，但还是不是保存数据库中
            comment = form.save(commit=False)

            #   将评论和被评论的文章关联起来 。
            comment.post = post

            #   最终将评论数据保存进数据库中，调用模型实例的 save 方法。
            comment.save()

            #   重定向到post的详情页，实际上当redirecr函数接收一个模型实例时候，
            #   然后重定向到get_absolute_url 方法返回的URL
            return redirect(post)

        else:
            #   检查到数据不合格，重新渲染详情页，并且渲染表单的错误
            #   因此我们传了三个模板变量给 detail.html,
            #   一个是文章Post，一个是评论列表，一个是表单form
            #   post.comment_set.all()查询文章下所有评论
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list
            }
            return render(request,'blog/detail.html',context=context)

        #不是post请求，说明用户没有提交数据，重定向到文章详情页
        return redirect(post)


