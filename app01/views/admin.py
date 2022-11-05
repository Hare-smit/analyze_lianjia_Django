from django.shortcuts import render,redirect
from django import forms
from app01 import models
from app01.static.part.pagination import Pagination
from app01.static.part.form import Admin_add,Admin_check

def admin_list(request):
    data_dict={}
    search_data = request.GET.get("q","")
    if search_data:
        data_dict["admin_user__contains"]=search_data


    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request,queryset,page_size=3,plus=2,)

    context = {
        "querset":page_object.page_queryset,
        "page_string":page_object.html(),
        "search_data":search_data,
        "title":"新建管理员"
    }
    return render(request,"admin_list.html",context)

def admin_add(request):
    if request.method=="GET":
        form = Admin_add()
        return render(request,"admin_add.html",{"title":"新建管理员","form":form})
    form = Admin_add(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "admin_add.html", {"title": "新建管理员", "form": form})

def admin_delete(request):
    nid = request.GET.get("nid")
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")

def admin_reset(request,nid):
    select_id = models.Admin.objects.filter(id=nid).first()
    if request.method=="GET":
        form = Admin_check(instance=select_id)
        return render(request,"admin_reset.html",{"title":"重置密码","form":form})
    form = Admin_check(data=request.POST,instance=select_id)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "admin_reset.html", {"title": "重置密码", "form": form})
