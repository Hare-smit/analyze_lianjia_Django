from django.db import models

# Create your models here.
class Admin(models.Model):

    def __str__(self):
        return self.admin_user

    admin_user = models.CharField(verbose_name="管理员",max_length=32)

    password = models.CharField(verbose_name="密码",max_length=256)

    plce = models.CharField(verbose_name="地区",max_length=64)

class plce(models.Model):

    plce = models.CharField(verbose_name="地区", max_length=64)

