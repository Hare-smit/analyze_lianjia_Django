from app01 import models
from django import forms
from warehouse.models import Housing
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.static.part.bootstrap import BootStrapModelForm
from app01.static.part.encrypt_md5 import md5
from funtinos.encrypt import RSA_encrypt,RSA_decrypt

#
# class User_run(BootStrapModelForm):
#     name=forms.CharField(min_length=2,label="用户名")
#
#     class Meta:
#         model = models.UserInfo
#         fields = ["id","name","password","age","create_time","gender","account","depart"]
#
# class Mobiles(BootStrapModelForm):
#     #正则表达式错误校验
#     mobile = forms.CharField(
#         label="手机号",
#         validators=[RegexValidator(r'^1[3-9]\d{9}$',"手机号格式错误")]
#     )
#
#     #mobile = forms.CharField(label="手机号",disabled=True)
#
#     class Meta:
#         model = models.Phone_number
#         #fields = ["mobile","price","level","status"]
#         fields = "__all__"
#         #exclude = ["level"]
#
#
#     #钩子方法校验
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#         exists = models.Phone_number.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
#         if exists:
#             raise ValidationError("手机号已存在")
#         return txt_mobile
#
# class Mobile(BootStrapModelForm):
#     #正则表达式错误校验
#     mobile = forms.CharField(
#         label="手机号",
#         validators=[RegexValidator(r'^1[3-9]\d{9}$',"手机号格式错误")]
#     )
#
#     class Meta:
#         model = models.Phone_number
#         #fields = ["mobile","price","level","status"]
#         fields = "__all__"
#         #exclude = ["level"]
#
#     #钩子方法校验
#     def clean_mobile(self):
#         txt_mobile = self.cleaned_data["mobile"]
#         exists = models.Phone_number.objects.filter(monile=txt_mobile).exists()
#         if exists:
#             raise ValidationError("手机号已经存在")
#         return txt_mobile

class Admin_add(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))

    class Meta:
        model=models.Admin
        fields = ["admin_user","password","confirm_password","plce"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

class Admin_check(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))

    class Meta:
        model=models.Admin
        fields = ["admin_user","password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        now_pwd=self.cleaned_data.get("password")
        exists = models.Admin.objects.filter(id=self.instance.pk,password=now_pwd).exists()
        if exists:
            raise ValidationError("不能重置最近使用的密码")
        return now_pwd


    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

class Login(BootStrapModelForm):
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True,
    )
    class Meta:
        model = models.Admin
        fields = ["admin_user","code","password"]
        widgets={
            "password":forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        print(pwd)
        return RSA_decrypt(pwd)



class Plce(BootStrapModelForm):
    class Meta:
        model= models.Admin
        fields=["plce"]


class House_type(BootStrapModelForm):

    class Meta:
        model= Housing
        fields = "__all__"
# class Order(BootStrapModelForm):
#     class Meta:
#         model = models.Order
#         fields = "__all__"
#         exclude=["order_num","admin"]
#
# class FileModelForm(BootStrapModelForm):
#     bootstrap_exclude_fields = ["img"]
#
#     class Meta:
#         model = models.City
#         fields = "__all__"
