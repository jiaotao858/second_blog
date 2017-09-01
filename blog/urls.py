from django.conf.urls import url
from .import views

#声明该url对应的APP
app_name = 'blog'

#视图与路由进行绑定
urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),  #文章地址页
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.ArchivesView.as_view(),name='archives'),    #归档地址页
    url(r'^category/(?P<pk>[0-9]+)/$',views.CategoryView.as_view(),name='category'),     #分类地址页
]