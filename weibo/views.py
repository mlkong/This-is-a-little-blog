from django.shortcuts import render,HttpResponse,redirect
from io import BytesIO
from weibo import models
from django.utils.safestring import mark_safe
import re
# Create your views here.



'''
判断是否登录SESSION,登陆页面、找回密码页面等用到
'''
def check_islogin(func):
    def check_login(request,*args,**kwargs):
        if request.session.get('is_session_login', False):
            return redirect('index.html')
        return func(request,*args,**kwargs)
    return check_login

'''
判断是否登录 个人管理中心用
'''
def per_islogin(func):
    def check_login(request,*args,**kwargs):
        # jump_url 记录跳转URL
        request.session['jump_url'] = request.get_full_path()
        if not request.session.get('is_session_login', False):
            # 记录跳转SESSION
            return redirect('login.html')
        else:
            return func(request,*args,**kwargs)
    return check_login

'''
判断是否有SESSION ++++ COOKIE，控制全站的昵称显示
'''
def check_login_session_cookie(func):
    def check_login(request,*args,**kwargs):
        global nickname_login_a
        # jump_url 记录跳转URL
        request.session['jump_url'] = request.get_full_path()
        if request.session.get('is_session_login', False):
            nickname_login = request.COOKIES.get('is_cookie_nickname',False)
            nickname_login_a = '<a href="personal.html" style="color:red;">'+ str(nickname_login.encode('latin-1').decode('utf-8'))+','+'欢迎您</a>'
        elif request.COOKIES.get('is_cookie_login',False):
            nickname_login = request.COOKIES.get('is_cookie_nickname',False)
            nickname_login_a = '<a href="login.html" style="color:red;">'+ str(nickname_login.encode('latin-1').decode('utf-8')) +','+'您好，请登录！</a>'
        else:
            nickname_login_a = """<a href='login.html' style='color:red;'>您好，请登录！</a>"""
        return func(request, *args, **kwargs)
    return check_login

'''
测试专用
'''
@check_login_session_cookie
def ceshi(request):
        return render(request, 'ceshi.html',{'nickname':mark_safe(nickname_login_a)})

'''
注销
'''
def cancell(request):
    if request.session['jump_url']:
        response = redirect(request.session['jump_url'])
    else:
        response = redirect('index.html')
    response.delete_cookie('is_cookie_cancell')
    request.session.clear()
    return response
'''
主页index
'''
from untis import pagination
@check_login_session_cookie
def index(request):
    categrys = models.ArticleCategory.objects.all().order_by('id')
    locaos = models.UserLocation.objects.all().order_by('id')
    # 筛选
    categry = int(request.GET.get('categry', 0))
    locao = int(request.GET.get('locao', 0))
    # 从数据中拿到文章信息
    if categry==0 and locao==0:
        articles = models.Articles.objects.all().order_by('-update_time')
    elif categry==0 and locao!=0:
        articles = models.Articles.objects.filter(article_location_id=locao).order_by('-create_time')
    elif categry != 0 and locao == 0:
        articles = models.Articles.objects.filter(article_category_id=categry).order_by('-create_time')
    else:
        articles = models.Articles.objects.filter(article_category_id=categry,article_location_id=locao).order_by('-create_time')
    # 分页
    current_page = int(request.GET.get('p', 1))
    page_obj = pagination.Page(current_page,len(articles))
    data = articles[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("index.html?&categry="+str(categry)+"&locao ="+str(locao))
    return render(request,'index.html',{'nickname':mark_safe(nickname_login_a),
                                        'data':data,
                                        'page_str':page_str,
                                        'categrys':categrys,
                                        'categry':categry,
                                        'locao':locao,
                                        'locaos':locaos})

'''
个人管理
'''
@per_islogin
def personal(request):
    hellow = request.COOKIES.get('is_cookie_nickname',False)
    hellow_a = '<a href="personal.html" style="color:red;">'+str(hellow.encode('latin-1').decode('utf-8'))+'，你好</a>'
    cancell_a = '<a href="cancell" >注销</a>'
    rel = int(request.GET.get('rel',1))
    username_artcle = ''
    artcle_location = ''
    artcle_categry = ''
    fans = ''
    fans_len = ''
    fllow = ''
    fllow_len = ''

    username = request.session['is_session_username']
    username_id = models.UserInfo.objects.filter(username=username)[0]
    if rel <= 1:
        rel = 1
        username_artcle = models.Articles.objects.filter(author_id = username_id.id).order_by('-create_time')
    elif rel == 2:
        fans = models.Fllows.objects.filter(fllow_id_id = username_id)
        fans_len = len(fans)
    elif rel == 3:
        fllow = models.Fllows.objects.filter(author_id_id=username_id)
        fllow_len = len(fllow)
    elif rel >= 4:
        rel = 4
        artcle_location = models.UserLocation.objects.all()
        artcle_categry = models.ArticleCategory.objects.all()

    dict_req = {
        'rel':rel,
        'username_artcle':username_artcle,
        'artcle_location':artcle_location,
        'artcle_categry':artcle_categry,
        'fans':fans,
        'fans_len':fans_len,
        'fllow':fllow,
        'fllow_len':fllow_len
    }
    return render(request, 'personal.html',{'hellow_a':mark_safe(hellow_a),
                                            'cancell_a':mark_safe(cancell_a),
                                            'dict_req':dict_req})
'''
文章删除处理函数
'''
def delete_artcle(request):
    artcle_id = request.POST.get('artcle_id')

    author_id = models.UserInfo.objects.filter(username = request.session['is_session_username'])[0].id
    if author_id != models.Articles.objects.filter(id = artcle_id)[0].author_id:
        return HttpResponse(201)
    models.Articles.objects.filter(author_id = author_id,id = artcle_id).delete()
    return  HttpResponse(200)

'''
文章发布
'''
def pub_text(request):
    title = request.POST.get('$title')
    if title =='':
        return HttpResponse(400)
    summary = request.POST.get('$summary')
    if summary =='':
        return HttpResponse(400)
    text = request.POST.get('$content')
    if text =='':
        return HttpResponse(400)
    artcle_location_id = request.POST.get('$location')
    if artcle_location_id =='':
        return HttpResponse(400)
    Category = request.POST.get('$pub_categary')
    if Category =='':
        return HttpResponse(400)
    author_id = models.UserInfo.objects.filter(username = request.session['is_session_username'])[0].id

    models.Articles.objects.create(title=title,
                                   summary=summary,
                                   text=text,
                                   article_location_id=artcle_location_id,
                                   author_id=author_id,
                                   article_category_id=Category)
    return HttpResponse(200)

'''
文章博主信息陈列
'''
@check_login_session_cookie
def author_info(request):
    # jump_url 记录跳转URL
    request.session['jump_url'] = request.get_full_path()
    author_id = int(request.GET.get('author_id', 1))
    rel = int(request.GET.get('rel', 1))
    fllow = models.Fllows.objects.filter(author_id_id=author_id)
    fllow_len = len(fllow)
    fans = models.Fllows.objects.filter(fllow_id_id=author_id)
    fans_len = len(fans)
    articles_info = ''
    author_info = models.UserInfo.objects.filter(id = author_id)

    if request.session.get('is_session_login', False):
        author_logi = request.session.get('is_session_username')
        author_login = int(models.UserInfo.objects.filter(username = author_logi)[0].id)
        if author_id == author_login:
            return redirect('personal.html')
        else:
            if models.Fllows.objects.filter(author_id_id = author_login):
                isfllow_or_no = '<em class="author_info_article_fllow author_info_article_fllow_isfllow_islogin" cancelled_author_id="%s">取消关注</em>'%author_id
            else:
                isfllow_or_no = '<em class="author_info_article_fllow author_info_article_fllow_nofllow_islogin" fllowed_author_id="%s">点击关注</em>'%author_id

            if rel <= 1:
                rel = 1
                articles_info = models.Articles.objects.filter(author_id=author_id).order_by('-create_time')
            elif rel == 2:
                pass
            elif rel >= 3:
                pass

            dict = {
                'rel': rel,
                'author_id': author_id,
                'articles_info': articles_info,
                'fllow': fllow,
                'fllow_len': fllow_len,
                'fans_len': fans_len,
                'fans': fans,
                'author_info': author_info,
                'isfllow_or_no':mark_safe(isfllow_or_no)
            }
            return render(request, 'author_info.html', {'nickname': mark_safe(nickname_login_a),
                                                        'dict': dict})
    # 如果没有登录干什么
    else:
        isfllow_or_no = '<em class="author_info_article_fllow author_info_article_fllow_nofllow_nologin">点击关注</em>'
        if rel <= 1:
            rel = 1
            articles_info = models.Articles.objects.filter(author_id=author_id).order_by('-create_time')
        elif rel == 2:
            pass
        elif rel >= 3:
            pass

    dict = {
        'rel':rel,
        'author_id':author_id,
        'articles_info':articles_info,
        'fllow':fllow,
        'fllow_len':fllow_len,
        'fans_len':fans_len,
        'fans':fans,
        'author_info':author_info,
        'isfllow_or_no':mark_safe(isfllow_or_no)
    }
    return render(request,'author_info.html',{'nickname':mark_safe(nickname_login_a),
                                              'dict':dict})

'''
没登录点击关注
'''
def nofllow_nologin(request):
    username = request.POST.get('username1','')
    passwd = request.POST.get('password1','')
    if username == '' or passwd== '':
        return HttpResponse(202)
    login1 =models.UserInfo.objects.filter(username = username,passwd = passwd)
    if login1:
        response = HttpResponse(200)
        # COOKIES是不能存中文的，否则报错！直到项目完成无意中用手机登陆才发现下面的BUG，很遗憾，只有这样假处理了，
        # 一个人不可能40年不换手机不换电脑，最长年限其实是2**31-1
        # 至于为什么设置这长是为了处理一个致命的BUG，由于最开始设计原因，导致SESSION在COOKIE失效，BOOL值login1[0].nickname.encode('utf-8').decode('latin-1')会报错
        response.set_cookie('is_cookie_login',True,max_age=2**30-1,path='/')
        # 控制注销按钮
        response.set_cookie('is_cookie_cancell', True, path='/')
        response.set_cookie('is_cookie_nickname',login1[0].nickname.encode('utf-8').decode('latin-1'),max_age=2**30-1,path='/')
        request.session['is_session_login'] = True
        request.session['is_session_username'] = login1[0].username
        return response
    else:
        return HttpResponse(201)
'''
登陆之后没关注
'''
def nofllow_islogin(request):
    login_author = models.UserInfo.objects.filter(username = request.session['is_session_username'])[0].id
    fllowed_author_id = request.POST.get('fllowed_author_id')
    models.Fllows.objects.create(author_id_id = login_author,fllow_id_id = fllowed_author_id)
    return HttpResponse(200)
'''
登陆之后关注了
'''
def isfllow_islogin(request):
    login_author = models.UserInfo.objects.filter(username=request.session['is_session_username'])[0].id
    cancelled_author_id = request.POST.get('cancelled_author_id')
    models.Fllows.objects.filter(author_id_id=login_author,fllow_id_id = cancelled_author_id).delete()
    return HttpResponse(200)

'''
文章详情页面
'''
@check_login_session_cookie
def details(request):
    login_id = ''
    artcles_id = int(request.GET.get('artcles_id'))
    # 数据库中那文章
    wenzhangs = models.Articles.objects.filter(id=artcles_id)
    read_mount = wenzhangs[0].read_mount+1
    wenzhangs.update(read_mount = read_mount )
    commits = models.Commit.objects.filter(commit_artcles_id= artcles_id).order_by('commit_time')
    commits2_total = models.Commit2.objects.filter(commit2_artcles_id= artcles_id)

    # jump_url 记录跳转URL
    request.session['jump_url'] = request.get_full_path()

    # 记录是否登录及是不是自己的来判断究竟显示删除按钮不
    if request.session.get('is_session_login'):
        login_id = models.UserInfo.objects.filter(username = request.session.get('is_session_username'))[0].id

    return render(request,'details.html',{'nickname':mark_safe(nickname_login_a),
                                          'wenzhangs':wenzhangs,
                                          'commits':commits,
                                          'commits2_total':commits2_total,
                                          'login_id':login_id
                                          })

# 删除评论1
def delete_commit1(request):
    delete_commit1_id = request.POST.get('delete_commit',1)

    login_id = models.UserInfo.objects.filter(username=request.session.get('is_session_username'))[0].id
    if login_id != models.Commit.objects.filter(id = delete_commit1_id)[0].commit_author_id:
        return HttpResponse(201)
    models.Commit.objects.filter(id = delete_commit1_id).update(commit_display = 0)
    return HttpResponse(200)
# 删除评论2
def delete_commit2(request):
    delete_commit2_id = request.POST.get('delete_commit',1)

    login_id = models.UserInfo.objects.filter(username=request.session.get('is_session_username'))[0].id
    if login_id != models.Commit2.objects.filter(id=delete_commit2_id)[0].commit2_author_id:
        return HttpResponse(201)
    models.Commit2.objects.filter(id=delete_commit2_id).update(commit2_display=0)
    return HttpResponse(200)

'''
提交评论处理函数
'''
def commit_submit(request):
    if not request.session.get('is_session_login', False):
        return HttpResponse(404)
    commit = request.POST.get('$val')
    if commit =='':
        return HttpResponse(400)
    commit_artcles = request.POST.get('$artcles_id')
    commit_author_nickname = request.session['is_session_username']
    commit_author = models.UserInfo.objects.filter(username=commit_author_nickname)[0].id

    # 增加评论
    wenzhangs = models.Articles.objects.filter(id = commit_artcles)
    commit_mount = wenzhangs[0].commit_mount+1
    wenzhangs.update(commit_mount = commit_mount)

    # 哎，查了很久还是不知道怎么处理高并发问题，只有这样伪处理了，因为MODELS设计了唯一
    def Concurrent1():
        try:
            floor_f = models.Commit.objects.filter(commit_artcles_id = commit_artcles).order_by('-commit_time')
            if floor_f:
                floor = floor_f[0].floor+1
            else:
                floor = 1

            dict = {
                'commit':commit,
                'commit_author_id':commit_author,
                'commit_artcles_id':commit_artcles,
                'floor':floor
            }
            models.Commit.objects.create(**dict)
            return HttpResponse(200)
        except:
            Concurrent1()
    Concurrent1()
    return HttpResponse(200)

def commit_submit2(request):
    if not request.session.get('is_session_login', False):
        return HttpResponse(404)
    commit2 = request.POST.get('$commit2')
    if commit2 =='':
        return HttpResponse(400)
    commit2_artcles_id = request.POST.get('$commit2_artcles_id')
    commit_author_nickname = request.session['is_session_username']
    commit_author = models.UserInfo.objects.filter(username=commit_author_nickname)[0].id
    commit2_to_commit1_id = request.POST.get('$commit2_to_commit1_id')

    wenzhangs = models.Articles.objects.filter(id=commit2_artcles_id)
    commit_mount = wenzhangs[0].commit_mount + 1
    wenzhangs.update(commit_mount=commit_mount)

    dic = {'commit2':commit2,
           'commit2_to_commit1_id':commit2_to_commit1_id,
           'commit2_artcles_id':commit2_artcles_id,
           'commit2_author_id':commit_author
           }
    models.Commit2.objects.create(**dic)
    return HttpResponse(200)

def commit_submit3(request):
    if not request.session.get('is_session_login', False):
        return HttpResponse(404)
    commit2 = request.POST.get('$commit2')
    if commit2 =='':
        return HttpResponse(400)
    commit2_artcles_id = request.POST.get('$commit2_artcles_id')
    commit_author_nickname = request.session['is_session_username']
    commit_author = models.UserInfo.objects.filter(username=commit_author_nickname)[0].id
    commit2_to_commit1_id = request.POST.get('$commit2_to_commit1_id')
    commit2_to_self_id = request.POST.get('$commit2_to_self_id')

    wenzhangs = models.Articles.objects.filter(id=commit2_artcles_id)
    commit_mount = wenzhangs[0].commit_mount + 1
    wenzhangs.update(commit_mount=commit_mount)

    dic = {'commit2':commit2,
           'commit2_to_commit1_id':commit2_to_commit1_id,
           'commit2_artcles_id':commit2_artcles_id,
           'commit2_author_id':commit_author,
           'commit2_to_self_id':commit2_to_self_id
           }
    models.Commit2.objects.create(**dic)
    return HttpResponse(200)

'''
验证码
'''
from untis.check_code import create_validate_code
def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

'''
登录页面
'''
@check_islogin
def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    elif request.method=='POST':
        username=request.POST.get('username')
        passwd=request.POST.get('passwd')
        check_code=request.POST.get('check_code').upper()
        message = {
            'username':username,
            'passwd':passwd
        }
        try:
            '''这里查不到会报错，也就是用户不存在'''
            login1 = models.UserInfo.objects.filter(username = username)[0]
            if login1.passwd == passwd:
                if check_code == request.session.get('CheckCode').upper():
                    if request.session.get('jump_url'):
                        response = redirect(request.session.get('jump_url'))
                    else:
                        response = redirect('/index.html')
                    response.set_cookie('is_cookie_login',True,max_age=2**30-1,path='/')
                    # 控制注销按钮
                    if request.POST.get('mianlogin', None) == '1':
                        response.set_cookie('is_cookie_cancell',True,path='/',max_age=60*60*24*7)
                    else:
                        response.set_cookie('is_cookie_cancell', True, path='/')
                    # COOKIES是不能存中文的，否则报错！直到项目完成无意中用手机登陆才发现下面的BUG，很遗憾，只有这样假处理了，
                    # 一个人不可能40年不换手机不换电脑，最长年限其实是2**31-1
                    # 至于为什么设置这长是为了处理一个致命的BUG，由于最开始设计原因，导致SESSION在COOKIE失效，BOOL值login1[0].nickname.encode('utf-8').decode('latin-1')会报错
                    response.set_cookie('is_cookie_nickname', login1.nickname.encode('utf-8').decode('latin-1'),max_age=2**30-1,path='/')

                    request.session['is_session_login'] = True
                    request.session['is_session_username'] = login1.username
                    if request.POST.get('mianlogin', None) == '1':
                        # 超时时间
                        request.session.set_expiry(60*60*24*7)
                    return response
                else:
                    check = '验证码错误,请重新输入！'
                    return render(request,'login.html',{'message':message,
                                                         'check': check})
            else:
                check='密码错误,请重新输入！'
                return render(request,'login.html',{'message':message,
                                                     'check':check})
        except:
            check = '用户名不存在,请重新输入'
            return render(request,'login.html',{'message':message,
                                                 'check': check})

'''
找回密码1
'''
@check_islogin
def backpw(request):
    datamess = '请仔细填写注册的部分信息，以便找回密码！'
    if request.method == 'GET':
        return render(request,'backpw.html',{'datamess':datamess})
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        data = {
            'username': username,
            'email': email,
            'nickname':nickname
        }
        if username == '' or email == '' or nickname == '':
            errors = '请把表填写完整哟!0！'
            return render(request, 'backpw.html',{'data':data,'errors':errors,'datamess':datamess})
        else:
            dic = {'username': username, 'email': email, 'nickname': nickname}
            datas = models.UserInfo.objects.filter(**dic)
            try:
                # 这里抓不住异常必须ELSE nickname == true  输入的True也能查到关键性信息必须比对
                if datas[0].username==username and datas[0].email==email and datas[0].nickname==nickname:
                    # 控制重置密码页面是否经过了此页面的验证
                    request.session['is_check_backpw'] = True
                    request.session['user_is_check'] = username
                    request.session.set_expiry(60)
                    return redirect('check_backpw.html')
                else:
                    errors = '信息不对，么么哒!2！'
                    return render(request, 'backpw.html', {'data': data,
                                                           'datamess': datamess,
                                                           'errors': errors})
            except:
                    errors = '信息不对哦，么么哒!！'
                    return render(request, 'backpw.html', {'data': data,
                                                           'datamess': datamess,
                                                           'errors':errors})
'''
找回密码2
'''
def check_backpw(request):
    if request.session.get('is_check_backpw',False):
        if request.method=='GET':
            return  render(request,'check_backpw.html')
        elif request.method=='POST':
            passwd1 = request.POST.get('passwd1')
            passwd2 = request.POST.get('passwd2')
            if passwd1==passwd2 and passwd1!= '' and passwd2 !='':
                req = '^[A-Za-z0-9]{6,12}$'
                reqsult = re.match(req,passwd1)
                if reqsult:
                    models.UserInfo.objects.filter(username=request.session['user_is_check']).update(passwd=passwd1)
                    data = '''
                    <h1><a id="aa" href="login.html">恭喜您密码修改成功，页面将在60s后跳转</a></h1>
                    <script type="text/javascript">
                        var aa=document.getElementById('aa');
                        var i = 59;
                        setInterval(function(){
                            aa.innerHTML='恭喜您密码修改成功，页面将在'+i+'s后跳转';
                            if(i==1){
                                window.location.href='login.html'
                            }
                            i = i-1;
                        },1000);
                    </script> 
                    '''
                    return HttpResponse(data)
                else:
                    data = '别搞小动作哦！！！不合法肯定过不了的哦！！！'
                    return render(request, 'check_backpw.html', {'data': data})
            else:
                data = '密码输入有误'
                return render(request, 'check_backpw.html',{'data':data})
    else:
        return redirect('backpw.html')

'''
注册页面
'''
from django import forms
from django.forms import widgets as Fwidgets
from django.forms import fields  as Ffields
from django.core.validators import RegexValidator

'''
注册页面form
'''
class FM(forms.Form):
    username = Ffields.CharField(
        error_messages={'required': '用户名不能为空.'},
        validators=[RegexValidator(r'^[0-9]+$', '请输入数字'), RegexValidator(r'^[0-9]{6,12}$', '只能6-12位数字')],
        widget=Fwidgets.TextInput(attrs={'class': 'c1','placeholder':"请输入用户名",'check_form':'false'}),
        label="用户名",
    )
    passwd1 = Ffields.CharField(
        max_length=12,
        min_length=6,
        validators=[RegexValidator(r'^[A-Za-z0-9]{6,12}$', '只能6-12位数字字母')],
        error_messages={'required': '密码不能为空.', 'min_length': '密码长度不能小于6', "max_length": '密码长度不能大于12'},
        widget=Fwidgets.PasswordInput(attrs={'class': 'c1','placeholder':"请输入密码",'check_form':'false'}),
        label = "密码",
    )
    passwd2 = Ffields.CharField(
        max_length=12,
        min_length=6,
        validators=[RegexValidator(r'^[A-Za-z0-9]{6,12}$', '只能6-12位数字字母')],
        error_messages={'required': '密码不能为空.', 'min_length': '密码长度不能小于6', "max_length": '密码长度不能大于12'},
        widget=Fwidgets.PasswordInput(attrs={'class': 'c1','placeholder':"请再次输入密码",'check_form':'false'}),
        label="确认密码",
    )
    phone = Ffields.CharField(
        error_messages={'required': '用户名不能为空.'},
        validators=[RegexValidator(r'^1[3|4|5|7|8]\d{9}$', '请输入正确的手机号')],
        widget=Fwidgets.TextInput(attrs={'class': 'c1','placeholder':"请输入手机号",'check_form':'false'}),
        label="手机",
    )
    nickname = Ffields.CharField(
        max_length=6,
        error_messages={'required': '昵称不能为空.', "max_length": '昵称长度不能大于6'},
        widget=Fwidgets.TextInput(attrs={'class': 'c1','placeholder':"请输入昵称",'check_form':'false'}),
        label="昵称",
    )
    email = Ffields.CharField(
        error_messages={'required': '邮箱不能为空.'},
        validators=[RegexValidator(r'^\w+([+-.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', '邮箱格式如qq@qq.com')],
        widget=Fwidgets.TextInput(attrs={'class': 'c1','placeholder':"请输入邮箱",'check_form':'false'}),
        label="邮箱",
    )

'''
注册页面处理函数
'''
def  register(request):

    location = models.UserLocation.objects.all()
    sex = models.UserSex.objects.all()

    if request.method=='GET':
        obj = FM()
        return render(request,'register.html',{'obj':obj,'sex':sex,'location':location})
    elif request.method=='POST':
        obj = FM(request.POST)
        r1 = obj.is_valid()
        if r1:
            username = request.POST.get('username')
            passwd1 = request.POST.get('passwd1')
            passwd2 = request.POST.get('passwd2')
            phone = request.POST.get('phone')
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')
            sex_id = request.POST.get('sex')
            location_id = request.POST.get('location')

            usernamerr = models.UserInfo.objects.filter(username=username)
            nicknamerr = models.UserInfo.objects.filter(nickname=nickname)
            exist = {}
            passwdrr = False
            if passwd1 != passwd2:
                passwdrr = True
                exist.setdefault('passwdrrs' , '对不起密码不一致')
            if usernamerr:
                usernamerrs = '对不起用户名存在'
            else:
                usernamerrs = ''
            if nicknamerr:
                nicknamerrs = '对不起，昵称已存在'
            else:
                nicknamerrs = ''
            if  usernamerr  or  nicknamerr or passwdrr:
                exist.setdefault('usernamerrs', usernamerrs)
                exist.setdefault('nicknamerrs', nicknamerrs)
                return render(request, 'register.html', {'obj': obj, 'sex': sex, 'location': location,'exist':exist})
            else:
                dic = {'username':username,
                       'passwd':passwd1,
                       'phone':phone,
                       'nickname':nickname,
                       'email':email,
                       'sex_id':sex_id,
                       'location_id':location_id,}
                models.UserInfo.objects.create(**dic)
                data = '''
                                    <h1><a id="aa" href="login.html">恭喜您密码修改成功，页面将在60s后跳转</a></h1>
                                    <script type="text/javascript">
                                        var aa=document.getElementById('aa');
                                        var i = 59;
                                        setInterval(function(){
                                            aa.innerHTML='恭喜您注册成功，页面将在'+i+'s后跳转';
                                            if(i==1){
                                                window.location.href='login.html'
                                            }
                                            i = i-1;
                                        },1000);
                                    </script> 
                                    '''
                return HttpResponse(data)
        else:
            return render(request, 'register.html',{'obj':obj,'sex':sex,'location':location})

'''
介绍
'''
@check_login_session_cookie
def introduce(request):
    cancell_a = ''
    if request.session.get('is_session_login', False):
        cancell_a = '<a href="cancell" >注销</a>'
    return render(request,'introduce.html',{'nickname':mark_safe(nickname_login_a),
                                            'cancell_a':mark_safe(cancell_a)})