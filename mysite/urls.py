"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from weibo import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 登录页
    url(r'^login.html$', views.login),
    # 验证码
    url(r'^check_code$', views.check_code),
    url(r'^ceshi.html$', views.ceshi),
    # 找回密码1
    url(r'^backpw.html$', views.backpw),
    # 找回密码2
    url(r'^check_backpw.html$', views.check_backpw),
    # 注册
    url(r'^register.html$', views.register),
    # 主页
    url(r'^index.html$', views.index),
    # 注销
    url(r'^cancell$', views.cancell),
    # 个人管理
    url(r'^personal.html$', views.personal),
    # 详细显示页面
    url(r'^details.html$', views.details),
    # 删除评论1
    url(r'delete_commit1',views.delete_commit1),
    #删除评论2
    url(r'delete_commit2',views.delete_commit2),
    # 删除文章
    url(r'delete_artcle$',views.delete_artcle),
    # 发布文章
    url(r'pub_text',views.pub_text),
    # 提交评论
    url(r'commit_submit$', views.commit_submit),
    url(r'commit_submit2$', views.commit_submit2),
    url(r'commit_submit3$', views.commit_submit3),
    # 作者信息陈列
    url(r'author_info.html',views.author_info),
    # 没登录点击关注
    url(r'nofllow_nologin',views.nofllow_nologin),
    # 登陆之后没有关注
    url(r'nofllow_islogin', views.nofllow_islogin),
    # 之路之后有关注
    url(r'isfllow_islogin',views.isfllow_islogin),
    # 本页及作者介绍
    url(r'introduce.html',views.introduce)
]
