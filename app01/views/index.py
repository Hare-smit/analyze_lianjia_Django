import os
import pandas as pd
import pymysql
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import View
from app01 import models
from app01.static.part.form import Plce
from warehouse.models import Housing
from funtinos.get_weather import *
from funtinos.get_location import *
#import subprocess
# Create your views here.



def lianjia_update(request):        #更新数据库--启用scrapy爬虫
    #Housing.objects.all().delete()
    os.system("scrapy crawl lianjia_scrapy")
    # subprocess.Popen('scrapy crawl lianjia_scrapy')
    return HttpResponse('OK')



# def print_cl(request,**kwargs):
#     context = kwargs if kwargs else {"html":None,"content":None}
#     return render(request,context["html"],context["content"])


# Create your views here.

def plce_edit(request):     #修改地区--更改的是用户地区
    if request.method=="GET":
        form = Plce()
        return render(request,"pl_choice.html",{"form":form,"title":"可视化分析地区"})

    name = request.session.get("info").get("name", "")
    pl_old = models.Admin.objects.filter(admin_user=name).first()
    form = Plce(data=request.POST, instance=pl_old)
    if form.is_valid():
        form.save()
        pl = pl_old.plce
    return redirect("/show/house/")


class index_main(View):     #类形式编写的全局分析页面
    # def get(self,request,*args,**kwargs):
    #     return print_cl(request,kwargs["html"],kwargs["content"])
    def get(self,request):
        name = request.session.get("info").get("name","")
        pl = models.Admin.objects.filter(admin_user=name).first().plce
        weather = get_weathers(pl)
        if pl:
            num = Housing.objects.filter(plce = f"{pl}").count()
            context = {"plce":pl,
                       "title":f"{pl}二手房数据分析平台",
                       "much":num,
                       "weather":weather["text"],
                       "temp":weather["temp"],
                       "img":f"/static/images/weather/{weather['text']}.png",
                       }
        #return self.get(**{"html":"index.html","content":{"title":f"{self.pl}二手房数据分析平台","much":num}})
            return render(request,"index.html",context)


        # else:
        #     form = Plce()
        #
        #     return render(request, "pl_choice.html",{"form":form})
    def post(self,request):
        # name = request.session.get("info").get("name", "")
        # pl_old = models.Admin.objects.filter(admin_user=name).first()
        #
        # form = Plce(data=request.POST,instance=pl_old)
        # if form.is_valid():
        #     form.save()
        return redirect("/list_vi")
#
# def get(self,request,*args):
#     #args=f"{index_main.pl}_cx.html"
#     return render(request,args)

@xframe_options_exempt
def cx(request):    #朝向饼图
    #html=f"{self.pl}_cx.html"
    name = request.session.get("info").get("name", "")
    pl = models.Admin.objects.filter(admin_user=name).first().plce
    return render(request,f"analyze_html/{pl}_cx.html")

@xframe_options_exempt
def zzt(request):       #小区房子平均价
    name = request.session.get("info").get("name", "")
    pl = models.Admin.objects.filter(admin_user=name).first().plce
    return render(request,f"analyze_html/{pl}_top10.html")

@xframe_options_exempt
def sdt(request):       #面积与总价散点图
    name = request.session.get("info").get("name", "")
    pl = models.Admin.objects.filter(admin_user=name).first().plce
    return render(request,f"analyze_html/{pl}_sdt.html")

@xframe_options_exempt
def hx(request):    #户型数量玫瑰饼图
    name = request.session.get("info").get("name", "")
    pl = models.Admin.objects.filter(admin_user=name).first().plce
    return render(request,f"analyze_html/{pl}_hx.html")

@xframe_options_exempt
def ditu(request):  #地图
    name = request.session.get("info").get("name", "")
    pl = models.Admin.objects.filter(admin_user=name).first().plce
    return render(request,f"analyze_html/{pl}_ditu.html")

def mean(request):  #导航栏
    name = request.session.get("info").get("name", "")
    pl = models.Admin.objects.filter(admin_user=name).first().plce
    return render(request,"test.html",{"pl":pl})

def main_home(request): #官方主页

    return render(request,"home_page.html")