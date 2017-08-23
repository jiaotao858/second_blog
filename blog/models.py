# -*- coding:utf-8 -*-

from django.db import models    #必须继承模型类
from django.contrib.auth.models import User     #自带的User模块
from django.utils.six import python_2_unicode_compatible    #兼容PY2 和 PY3
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

#文章类别Category
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self): # __str__显示返回的内容
        return self.name

#文章的标签
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#文章的内容
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0) #统计阅读数量

    def __str__(self):
        return self.title

    #约定俗成的方法获取文章url
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    # 复写save方法
    def save(self,*args,**kwargs):
        #如果没有填写再要
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codelilite'
            ])
            #先将Markdown 文本渲染成HTML文本
            #strip_tag 去掉全部HTML标签
            #从文本中摘取54个字符赋excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Post,self).save(*args,**kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    #内部内 Meta方法显示
    class Meta:
        ordering = ['-create_time','title']



