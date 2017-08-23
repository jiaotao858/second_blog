# -*- coding:utf-8 -*-

from django.db import models    #必须继承模型类
from django.contrib.auth.models import User     #自带的User模块
from django.utils.six import python_2_unicode_compatible    #兼容PY2 和 PY3
from django.urls import reverse

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

    def __str__(self):
        return self.title

    #约定俗成的方法获取文章url
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    #内部内 Meta方法显示
    class Meta:
        ordering = ['-create_time','title']

