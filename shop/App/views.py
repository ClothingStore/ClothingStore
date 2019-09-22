from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse

from App import models
from App.models import Clothing, Order, Clothingdetail, Section, Salesreturn, Member, Superuserg
from shop.settings import MDEIA_ROOT
from tools.fileupload import FileUpload
from tools.mypaginator import MyPaginator


def index(request):

    return render(request,'admin/index.html')

#后台登录
def login(request):
    if request.method == "POST":
        print(1)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Superuserg.objects.filter(username=username).first()
        if user :
            print(user.password)

        else:
            print('cw')
            return render(request, 'admin/login.html')
        if user.password==password:

            return redirect('app:index')
        return render(request, 'admin/login.html')

    return render(request, 'admin/login.html')

#商品列表
def product_list(request,page=1):
    if request.GET.get('sid' ) == '20':
        datas=Clothing.objects.filter(sid=20)
        # print(datas)
    elif request.GET.get('sid')=='1':

        datas=Clothing.objects.filter(sid__grade=1).filter(is_del=0)
    elif request.GET.get('sid')=='2':
        datas=Clothing.objects.filter(sid__grade=2).filter(is_del=0)
    elif request.GET.get('sid')=='3':
        datas=Clothing.objects.filter(sid__grade=3).filter(is_del=0)
    else:
        datas=Clothing.objects.filter(is_del=0)
    per_page = 5
    paginator = MyPaginator(datas, per_page, number=int(page))
    pagination = paginator.page()
    total = datas.count()

    starts = ((int(page) - 1) * per_page + 1, int(page) * per_page)
    # print(datas)
    return render(request,'admin/product_list.html',locals())


def product_detail(request,cid):

    data=Clothing.objects.filter(cid=cid).first()
    photo=Clothingdetail.objects.filter(cid=cid).first()
    fenlei=Section.objects.all()
    flb=Section.objects.filter(sid=data.sid.sid).first()
    if request.method == 'POST':
        path = MDEIA_ROOT

        cothing = Clothing.objects.filter(cid=cid).first()
        # 各字段
        cothing.productid = request.POST.get('ppid')
        cothing.cname = request.POST.get('cname')
        cothing.data = datetime.now()
        cothing.number = request.POST.get('number')
        cothing.size = request.POST.get('size')
        cothing.color = request.POST.get('color')
        cothing.price = request.POST.get('price')
        cothing.sid = Section.objects.get(sid=request.POST.get('fenlei'))

        cothing.save()
        cothid = Clothing.objects.last()
        detail = Clothingdetail.objects.filter(cid=cid).first()


        file_photo = request.FILES.get('p1')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview1 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p2')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview2 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p3')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview3 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p4')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview4 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p5')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview5 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p6')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.drawing = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p7')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.detailed = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p8')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.modeled = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        detail.save()
    return render(request,'admin/product_detail.html',locals())


def add_product(request):
    datas=Section.objects.all()
    if request.method == 'POST':
        path = MDEIA_ROOT

        cothing = Clothing()
        # 各字段
        cothing.productid = request.POST.get('ppid')
        cothing.cname = request.POST.get('cname')
        cothing.data = datetime.now()
        cothing.number = request.POST.get('number')
        cothing.size = request.POST.get('size')
        cothing.color = request.POST.get('color')
        cothing.price = request.POST.get('price')
        cothing.sid = Section.objects.get(sid=request.POST.get('fenlei'))
        cothing.is_del =0
        cothing.save()
        cothid = Clothing.objects.last()
        detail = Clothingdetail()
        detail.cid = cothid
        file_photo = request.FILES.get('p1')
        if  file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview1 ='https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/'+ str(obj.file_name)
        file_photo = request.FILES.get('p2')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview2 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p3')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview3 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p4')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview4 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p5')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.preview5 = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p6')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.drawing = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p7')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.detailed = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        file_photo = request.FILES.get('p8')
        if file_photo:
            obj = FileUpload(file_photo, is_randomname=True)
            obj.upload(path)
            detail.modeled = 'https://cothingdetail-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
        detail.save()
    return render(request,'admin/add_product.html',locals())


def delete_product(request,cid):
    data=Clothing.objects.filter(cid=cid).first()

    data.is_del=1

    data.save()
    return redirect(reverse('app:product_list'))


def order_list(request):
    if request.GET.get('is_payment')=='1':
        datas=Order.objects.filter(is_payment=0).filter(is_back=0)
    elif request.GET.get('is_status')=='0':
        datas=Order.objects.filter(is_status=0).filter(is_payment=1).filter(is_back=0)
    elif request.GET.get('is_status')=='1':
        datas=Order.objects.filter(is_status=1).filter(is_take=0).filter(is_back=0)
    elif request.GET.get('is_take')=='1':
        datas=Order.objects.filter(is_take=1).filter(is_back=0)
    else:
        datas=Order.objects.filter(is_back=0)
    return render(request,'admin/order_list.html',locals())


def order_detail(request,id):
    if request.GET.get('is_take')=='1':
        take=Order.objects.get(id=id)
        take.is_status=1
        take.save()

    data = Order.objects.filter(id=id).first()

    clothing=Clothing.objects.filter(cid=data.cid.cid).first()

    return render(request,'admin/order_detail.html',locals())


def user_list(request):
    datas=Member.objects.all()
    return render(request,'admin/user_list.html',locals())


def user_detail(request,uid):
    data=Member.objects.filter(uid=uid).first()

    return render(request,'admin/user_detail.html',locals())


def user_rank(request):
    return render(request,'admin/user_rank.html')


def web_site(request):
    return render(request,'admin/setting.html')


def order_back(request):
    if request.GET.get('is_back')=='1':
        datas=Order.objects.filter(is_back=1)
    elif request.GET.get('is_back')=='2':
        datas=Order.objects.filter(is_back=2)
    else:
        datas=Order.objects.filter(is_back__gt=0)
    return render(request,'admin/orderback_list.html',locals())


def delproduct_list(request,page=1):
    datas=Clothing.objects.filter(is_del=1)
    per_page = 5
    paginator = MyPaginator(datas, per_page, number=int(page))
    pagination = paginator.page()
    total = datas.count()

    starts = ((int(page) - 1) * per_page + 1, int(page) * per_page)

    return render(request,'admin/productdel_list.html',locals())


def recover_product(request,cid):
    data=Clothing.objects.filter(cid=cid).first()
    data.is_del=0
    data.save()

    return redirect(reverse('app:delproduct_list'))


def orderback_detail(request,id):
    if request.GET.get('is_back')=='2':
        yes=Order.objects.filter(id=id).last()
        yes.is_back=2
        yes.save()
        yess=Salesreturn.objects.filter(oid=yes.id).last()
        yess.state=1
        yess.save()
    if request.GET.get('is_back')=='0':
        dont=Order.objects.filter(id=id).last()
        dont.is_back=0
        dont.save()
        dontt=Salesreturn.objects.filter(oid=dont.id).last()
        dontt.state=2
        dontt.save()
    data = Order.objects.filter(id=id).first()

    clothing = Clothing.objects.filter(cid=data.cid.cid).first()
    back=Salesreturn.objects.filter(oid=id).first()
    return render(request,'admin/orderback_detail.html',locals())


def logout(request):
    return render(request,'admin/login.html')