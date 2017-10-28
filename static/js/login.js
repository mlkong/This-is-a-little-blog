$(function () {
    // 点击更换验证码
    $(".check_code_img").click(function () {
        $(this).attr('src',$(this).attr('src')+'?')
    });
        
//登陆页面JS开始
    (function () {
            // 登陆按钮变色
    $('.login_main_form_dengluipu').mouseenter(function () {
        $('.login_main_form_denglu').css('backgroundColor','red')
    }).mouseleave(function () {
        $('.login_main_form_denglu').css('backgroundColor','darkseagreen')
    })

    // 获得焦点隐藏错误提示
    $('#username,#passwd,#check_code').focus(function () {
        $('.errors').html('');
    })

    // 免登陆弹出警告
    $('.login_main_form_miandenglu>input').click(function () {
        if($(this).is(":checked")){
            if(window.confirm('确认一月免登陆吗？')!=true){
                $(this).prop('checked',false)
            }
        }
    })

    // 登录验证
    $('.login_main_form_dengluipu').click(function () {
        var result=false;
        $('.check_null').each(function (index,ele) {
            if($(ele).val()==''){
                $('.errors').html('请填写完整在提交哦，么么哒！');
                result=true;
                return false;
            };
        });
        if (result){
            return false;
        }
    })
    })();
    // 登陆页面JS结束

    // 找回密码的JS开始
    (function () {
            // 检查表单是否有误
    $('.backpw_mid_big3_ul1>li .submitt').click(function () {
        var result=false;
        $('.check_null').each(function (index,ele) {
            if($(ele).val()==''){
                $('.backpw_mid_big3_ul1>li span').html('请填写完整再提交哦。');
                result=true;
                return false;
            };
        });
        if (result){
            return false;
        }else {
            var req = /^[A-Za-z0-9]{6,12}$/;
            var re = new RegExp(req);
            var $pwd1 = $('.backpw_mid_big3_ul1 #passwd1').val();
            var $pwd2 = $('.backpw_mid_big3_ul1 #passwd2').val();
            if (re.test($pwd1) && re.test($pwd2)) {
                result=false;
            } else {
                $('.backpw_mid_big3_ul1>li span').html('亲，格式6-12位字母数字');
                return false;
            };
            if ($pwd1 != $pwd2) {
                $('.backpw_mid_big3_ul1>li span').html('密码不一致！！');
                return false;
            };
        }
    });
        // 获得焦点隐藏错误提示
    $('.backpw_mid_big3_ul1>li .check_null').focus(function () {
        $('.backpw_mid_big3_ul1>li span').html('');
    });
    })();
    // 找回密码的JS结束
    
    // 注册页面开始
    (function () {
    // 点击清空各项错误信息
    // $('.c1').focus(function () {
    //     $(this).next('span').html('');
    // });
    // 表单验证
    //     input check_form  = true;属性判断是否合格
     $('.register_mid_mid .form_register .c1').on('input propertychange',function () {
         if($(this).attr('id') == 'id_username'){
             var req = /^[0-9]{6,12}$/;
             var re = new RegExp(req);
             if( !re.test($(this).val())){
                 $(this).attr('check_form','true');
                 $(this).next('span').html('用户名是6-12位数字哦！');
             }else {
                 $(this).attr('check_form','false');
                 $(this).next('span').html('');
             }
         }else if($(this).attr('id') == 'id_passwd1'){
            var req = /^[A-Za-z0-9]{6,12}$/;
            var re = new RegExp(req);
             if( !re.test($(this).val())){
                 $(this).attr('check_form','true');
                 $(this).next('span').html('密码6-12位字母数字！');
             }else {
                 if($(this).val() == $('#id_passwd2').val()){
                    $(this).attr('check_form','false');
                    $('#id_passwd2').attr('check_form','false');
                    $(this).next('span').html('');
                    $('#id_passwd2').next('span').html('');
                 }else {
                     $('#id_passwd2').attr('check_form','true');
                     $(this).next('span').html('两次密码要一样哦！');
                 }
             }
         }else if($(this).attr('id') == 'id_passwd2'){
            var req = /^[A-Za-z0-9]{6,12}$/;
            var re = new RegExp(req);
             if( !re.test($(this).val())){
                 $(this).attr('check_form','true');
                 $(this).next('span').html('密码6-12位字母数字！');
             }else {
                 if($(this).val() == $('#id_passwd1').val()){
                    $(this).attr('check_form','false');
                    $('#id_passwd1').attr('check_form','false');
                    $(this).next('span').html('');
                    $('#id_passwd1').next('span').html('');
                 }else {
                     $('#id_passwd1').attr('check_form','true');
                     $(this).next('span').html('两次密码要一样哦！');
                 }
             }
         }else if($(this).attr('id') == 'id_phone'){
            var req = /^1[3|4|5|7|8]\d{9}$/;
            var re = new RegExp(req);
             if( !re.test($(this).val())){
                 $(this).attr('check_form','true');
                 $(this).next('span').html('手机号不要乱输入嘛！');
             }else {
                 $(this).attr('check_form','false');
                 $(this).next('span').html('');
             }
         }else if($(this).attr('id') == 'id_nickname'){
             if($(this).val().length<1|| $(this).val().length>6){
                 $(this).attr('check_form','true');
                 $(this).next('span').html('昵称不得大于6位！');
             }else {
                 $(this).attr('check_form','false');
                 $(this).next('span').html('');
             }
         }else if($(this).attr('id') == 'id_email'){
            var req = /^\w+([+-.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
            var re = new RegExp(req);
             if( !re.test($(this).val())){
                 $(this).attr('check_form','true');
                 $(this).next('span').html('请输入正确的邮箱格式！');
             }else {
                 $(this).attr('check_form','false');
                 $(this).next('span').html('');
             }
         }
     })
    // 控制是否提交表单
     $('.register_mid_mid .form_register .subumit').click(function () {
        var result = false;
        var check_form=false;
        $('.register_mid_mid .form_register .c1').each(function (i,e) {
            if($(e).val() == ''){
                result = true;
                $(e).next('span').html('这里不能为空哦！');
            };
            if($(e).attr('check_form') == 'true'){
                check_form=true;
            }
        });
        if (result || check_form){
            alert("请详细核对表单");
            return false;
        }
    })
    })();
    // 注册页面结束

        // 主页开始
        // 控制筛选
    $('.index_mid_maxbig .index_mid_ul >li a').click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    });
    // 主页结束

    // 详情页开始
    // 提交评论
    $('.details_mid_combutton a').click(function () {
        var $val = $('.details_mid_combutton .commit_text').val();
        // al().replace(/[\n\r]/g,'<br>'
        var $artcles_id = $('.details_mid_combutton .commit_text').attr('artcles_id');
        if ($val == ''){
            alert('对不起文章评论不能为空！');
            return false;
        }
        $.ajaxSetup({
                beforeSend: function(xhr,settings){
                    xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'));
                }
            });
        $.ajax({
            url:'/commit_submit',
            type:'POST',
            data:{'$val':$val,'$artcles_id':$artcles_id},
            // headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            success:function (data) {
                if (data == 404){
                    window.location.href='login.html';
                }else if(data ==200){
                    window.location.reload();
                }else if(data ==400){
                    alert('对不起文章评论不能为空！');
                }
            }
        })
    });
    $('.submit_one').each(function (i,e) {
        $(e).on('click',function () {
            var ahtm = $('.replay_layer').eq(i);
            var $commit2_to_commit1_id = ahtm.attr('commit___1_line_id');
            var $commit2_artcles_id =ahtm.attr('artcles_id');
            var $commit2 = $(e).prev().val();

            if ($commit2 == ''){
            alert('对不起文章评论不能为空！');
            return false;
        }
        $.ajaxSetup({
                beforeSend: function(xhr,settings){
                    xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'));
                }
            });
        $.ajax({
            url:'/commit_submit2',
            type:'POST',
            data:{'$commit2':$commit2,
                '$commit2_artcles_id':$commit2_artcles_id,
                '$commit2_to_commit1_id':$commit2_to_commit1_id},
            success:function (data) {
                if (data == 404){
                    window.location.href='login.html';
                }else if(data ==200){
                    window.location.reload();
                }else if(data ==400){
                    alert('对不起文章评论不能为空！');
                }
            }
        })

        })
    });
    $('.submit_two').each(function (i,e) {
        $(e).on('click',function () {
            var $commit2_to_commit1_id = $('.two_layer_submit').eq(i).attr('two_to_on_id');
            var $commit2_artcles_id =$('.two_layer_submit').eq(i).attr('artcles_id');
            var $commit2_to_self_id = $('.two_layer_submit').eq(i).attr('author_who');
            var $commit2 = $(e).prev().val();

            if ($commit2 == ''){
            alert('对不起文章评论不能为空！');
            return false;
        }
        $.ajaxSetup({
                beforeSend: function(xhr,settings){
                    xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'));
                }
            });
        $.ajax({
            url:'/commit_submit3',
            type:'POST',
            data:{'$commit2':$commit2,
                '$commit2_artcles_id':$commit2_artcles_id,
                '$commit2_to_commit1_id':$commit2_to_commit1_id,
                '$commit2_to_self_id':$commit2_to_self_id},
            success:function (data) {
                if (data == 404){
                    window.location.href='login.html';
                }else if(data ==200){
                    window.location.reload();
                }else if(data ==400){
                    alert('对不起文章评论不能为空！');
                }
            }
        })

        })
    });
    // 提交评论结束

    // 删除评论1
    $('.delete_commit1').on('click',function () {
        $.ajax({
            url:'delete_commit1',
            type:'POST',
            data:{'delete_commit':$(this).attr('delete_commit')},
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            success:function (data) {
                    if(data==200){
                        window.location.reload();
                    }else if(data ==201){
                        alert('别搞小动作，你是删不了其他人的！哈哈，傻逼了吧！装逼了吧！')
                    }
            }
        });
    });
    // 删除评论2
    $('.delete_commit2').on('click',function () {
        $.ajax({
            url:'delete_commit2',
            type:'POST',
            data:{'delete_commit':$(this).attr('delete_commit')},
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            success:function (data) {
                    if(data==200){
                        window.location.reload();
                    }else if(data ==201){
                        alert('别搞小动作，你是删不了其他人的！哈哈，傻逼了吧！装逼了吧！');
                    }
            }
        });
    });

    // 控制评论框显示隐藏
    $('.two_layer_submit').each(function (i,e) {
        $(this).click(function () {
            $('.button_div_2').eq(i).css('display','block');
        })
    });
    $('.button_pubr').each(function (i,e) {
        $(this).click(function () {
            $(this).parent().css('display','none');
        })
    });
    $('.replay_layer').each(function (i,e) {
        $(this).click(function () {
            $('.button_div_1').eq(i).css('display','block');
        })
    });
    // 控制评论框显示隐藏
    // 详情页结束


    // 个人管理开始
    // 删除文章
    $('.delete_artcle').each(function (i,e) {
        $(e).on('click',function (event) {
            $('.person_mid_a').each(function (i,e) {
                $(e).click(function () {
                    return false;
                })
            });//接触a标签默认跳转
        if(window.confirm('确认删除这篇文章吗')!=true){
            $('.person_mid_a').unbind('click');
            return false;
        };
        var artcle_id = $(e).parent().parent().parent().attr('artcles_id');
        $.ajaxSetup({
            beforeSend: function(xhr,settings){
                xhr.setRequestHeader('X-CSRFtoken', $.cookie('csrftoken'));
            }
        });
        $.ajax({
              url:'delete_artcle',
              type:'POST',
              data:{'artcle_id':artcle_id},
              success:function (data) {
                  if (data == 404){
                      $('.person_mid_a').unbind('click');
                      window.location.href='login.html';
                  }else if(data ==200){
                      $('.person_mid_a').unbind('click');
                      window.location.reload();
                  }else if(data == 201){
                      alert('别搞小动作，你是删不了其他人的！哈哈，傻逼了吧！装逼了吧！')
                  }
              }
          });
        })
    });
    // 发布文章
    $('.pub_text_button').on('click',function () {
        var $title = $('.person_mid4_div .pub_title').val();
        var $location = $('.person_mid4_div .pub_location').val();
        var $summary = $('.person_mid4_div .pub_summary').val();
        var $content = $('.person_mid4_div .pub_content').val();
        var $pub_categary = $('.person_mid4_div .pub_categary').val();

        var  is_pub = true;
        $('.pub_jqeach').each(function (i,e) {
           if($(e).val() == ''){
               alert('对不起文章不能为空！')
               is_pub = false;
               return false;
           }
        });
        if (!is_pub){
            return false;
        }
        $.ajax({
            url:'pub_text',
            type:'POST',
            data:{
                '$title':$title,
                '$location':$location,
                '$summary':$summary,
                '$content':$content,
                '$pub_categary':$pub_categary
            },
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            success:function (data) {
                if (data == 404){
                    window.location.href='login.html';
                }else if(data ==200){
                    $('.person_mid_maxbig').html('<a href="personal.html?rel=4" style="margin:20px; ">继续发布</a>' +
                        '<a href="personal.html?rel=1" style="margin:20px;">回到我的文章</a>')
                }else if(data ==400){
                    alert('对不起文章评论不能为空！');
                }
            }
        })
    });
   // 个人管理结束

    // 作者信息陈列开始
    // 没登录点击关注 弹出登录框 下面是登录框的事件
    $('.author_info_is_login_div1first').click(function () {
        $('.author_info_is_login').css('display','none');
    });
    $('.author_info_is_login_in').focus(function () {
        $('.author_info_is_login_p').html('');
    });
    $('.author_info_is_login_div1_button').click(function () {
        var is_true = true;
        $('.author_info_is_login_in').each(function (i,e) {
            if($(e).val()==''){
                is_true=false;
                return false;
            }
        });
        if (!is_true){
            $('.author_info_is_login_p').html('请把表单填写完整');
            return false;
        };
        $.ajax({
            url:'nofllow_nologin',
            type:'POST',
            data:{
                'username1':$('.author_info_username1').val(),
                'password1':$('.author_info_password1').val()
            },
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            success:function (data) {
                if(data ==200){
                    window.location.reload();
                }else if(data ==201){
                    $('.author_info_is_login_p').html('用户名或密码错误');
                }else if(data == 202){
                    $('.author_info_is_login_p').html('给你说不能空！');
                }
            }
        });
        return false;
    });
    $('.author_info_article_fllow_nofllow_nologin').on('click',function () {
        $('.author_info_is_login').css('display','block');
    });

    //登陆之后没有关注
    $('.author_info_article_fllow_nofllow_islogin').click(function () {
        $.ajax({
            url:'nofllow_islogin',
            type:'POST',
            data:{'fllowed_author_id':$(this).attr('fllowed_author_id')},
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            success:function (data) {
                    window.location.reload();
            }
        });
    });
    //登陆之后有关注
    $('.author_info_article_fllow_isfllow_islogin').click(function () {
        $.ajax({
            url:'isfllow_islogin',
            type:'POST',
            data:{'cancelled_author_id':$(this).attr('cancelled_author_id')},
            headers: {'X-CSRFtoken': $.cookie('csrftoken')},
            success:function (data) {
                    window.location.reload();
            }
        });
    });
    // 作者信息陈列结束
});
