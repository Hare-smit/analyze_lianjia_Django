from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from app01 import models
from django.shortcuts import render,redirect,HttpResponse
from app01.static.part.form import Login
from app01.static.part.code import check_code
from io import BytesIO




def login(request):
    with open("/Users/huanghanhua/PycharmProjects/analyze_lianjia_Django/funtinos/rsa.public.pem", mode="r") as f:
        pub_key = f.read()      #公钥
    if request.method=="GET":
        form = Login()
        return render(request,"login.html",{"form":form,"pub_key":pub_key}) #get请求进入登录页
    # print(pub_key)
    form = Login(data=request.POST)     #获取post请求中的信息
    if form.is_valid():
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code","")#可能因为过时没有了所以获取时候为none这里设置让他为""
        if code.upper() != user_input_code.upper():
            form.add_error("code","验证码输入不正确")
            return render(request, "login.html", {"form": form,"pub_key":pub_key})
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password","用户名或者密码不正确")
            return render(request, "login.html", {"form": form,"pub_key":pub_key})
        pl = models.Admin.objects.filter(admin_user=admin_obj.admin_user).first().plce
        request.session["info"] = {"id":admin_obj.id,"name":admin_obj.admin_user,"plce":pl}
        #session设置了保留7天
        request.session.set_expiry(60*60*24*7)
        return redirect("/main/home/")

    return render(request, "login.html", {"form": form,"pub_key":pub_key})



# def login(request):
#     """ 登录 """
#     if request.method == "GET":
#         form = Login()
#         return render(request, 'login.html', {'form': form})
#
#     form = Login(data=request.POST)
#     if form.is_valid():
#         # 验证成功，获取到的用户名和密码
#         # {'username': 'wupeiqi', 'password': '123',"code":123}
#         # {'username': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f',"code":xxx}
#
#         # 验证码的校验
#         user_input_code = form.cleaned_data.pop('code')
#         code = request.session.get('image_code', "")
#         if code.upper() != user_input_code.upper():
#             form.add_error("code", "验证码错误")
#             return render(request, 'login.html', {'form': form})
#
#         # 去数据库校验用户名和密码是否正确，获取用户对象、None
#         # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
#         admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
#         if not admin_object:
#             form.add_error("password", "用户名或密码错误")
#             # form.add_error("username", "用户名或密码错误")
#             return render(request, 'login.html', {'form': form})
#
#         # 用户名和密码正确
#         # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
#         request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
#         # session可以保存7天
#         request.session.set_expiry(60 * 60 * 24 * 7)
#         return redirect("/admin/list/")
#     return render(request, 'login.html', {'form': form})



def logout(request):
    request.session.clear()
    return redirect("/login/")

def image_code(request):
    #调用pillow函数生成图片
    img,code_string = check_code()

    #写入session中（以便后续获取验证码再进行校验）
    request.session["image_code"]=code_string
    #给session 设置60s超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream,"png")
    #stream.getvalue()
    return HttpResponse(stream.getvalue())


# def image_code(request):
#     """ 生成图片验证码 """
#
#     # 调用pillow函数，生成图片
#     img, code_string = check_code()
#
#     # 写入到自己的session中（以便于后续获取验证码再进行校验）
#     request.session['image_code'] = code_string
#     # 给Session设置60s超时
#     request.session.set_expiry(60)
#
#     stream = BytesIO()
#     img.save(stream, 'png')
#     return HttpResponse(stream.getvalue())