from django.db import models
import django.utils.timezone as timezone
# Create your models here.
# 用户信息表
class UserInfo(models.Model):
    username=models.CharField(max_length=32,unique=True,null=False)
    passwd = models.CharField(max_length=32,null=False)
    email=models.CharField(max_length=32,null=False)
    nickname=models.CharField(max_length=32,null=False,unique=True)
    phone = models.CharField(max_length=32,null=False)

    location = models.ForeignKey(to='UserLocation',to_field='id',on_delete=models.CASCADE)
    sex = models.ForeignKey(to='UserSex', to_field='id',on_delete=models.CASCADE)

# 地址表
class UserLocation(models.Model):
    locations = models.CharField(max_length=32,null=False)

# 性别表
class UserSex(models.Model):
    sex =models.CharField(max_length=32,null=False)

# 文章分类表
class ArticleCategory(models.Model):
    Category = models.CharField(max_length=32,unique=True,null=False)

# 文章表
class Articles(models.Model):
    title = models.TextField(null=False)
    summary = models.TextField(null=False)
    text = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True,null=True)
    update_time = models.DateTimeField(auto_now=True,null=True)
    read_mount = models.IntegerField(null=False,default=0)
    commit_mount = models.IntegerField(null=False,default=0)

    author = models.ForeignKey(to='UserInfo',to_field='id',on_delete=models.CASCADE)
    article_location = models.ForeignKey(to='UserLocation', to_field='id',on_delete=models.CASCADE)
    article_category = models.ForeignKey(to='ArticleCategory', to_field='id',on_delete=models.CASCADE)

 # 评论表1
class Commit(models.Model):
    commit = models.TextField(null=False)
    commit_time = models.DateTimeField(auto_now_add=True,null=True)
    commit_display = models.IntegerField(null=False,default=1)
    floor = models.IntegerField(null=True,default=0)

    commit_author = models.ForeignKey(to='UserInfo', to_field='id',on_delete=models.CASCADE)
    commit_artcles = models.ForeignKey(to='Articles', to_field='id',on_delete=models.CASCADE)

    # 以便VIEWS高并发显示楼层的伪处理,哎，只有这样实现了。
    class Meta:
        unique_together = [
            ('floor', 'commit_artcles'),
        ]

# 评论表2
class Commit2(models.Model):
    commit2 = models.TextField(null=False)
    commit2_time = models.DateTimeField(auto_now_add=True,null=True)
    commit2_display = models.IntegerField(null=False,default=1)

    commit2_author = models.ForeignKey(to='UserInfo', related_name='commit2_author_back',to_field='id',on_delete=models.CASCADE)
    commit2_artcles = models.ForeignKey(to='Articles', to_field='id',related_name='commit2_artcles_back',on_delete=models.CASCADE)
    commit2_to_commit1 = models.ForeignKey(to='Commit',to_field='id',related_name='commit2_to_commit1_back',on_delete=models.CASCADE)
    commit2_to_self = models.ForeignKey(to='self',related_name='commit2_to_self_back',null=True,on_delete=models.CASCADE)

# 粉丝及关注关系表
class Fllows(models.Model):
    author_id = models.ForeignKey(to='UserInfo',to_field='id',related_name='author_to_fllows',null=True,on_delete=models.CASCADE)
    fllow_id = models.ForeignKey(to='UserInfo', to_field='id',related_name='fllow_to_author',null=True,on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('author_id', 'fllow_id'),
        ]