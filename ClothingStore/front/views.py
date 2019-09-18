from random import randint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

# Create your views here.
from django.urls import reverse

from ClothingStore.settings import MDEIA_ROOT
from front.form import RegisterForm, LoginForm, AddressForm
from front.models import *
from tools.fileupload import FileUpload


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = '新用户' + str(randint(100000, 999999))
            Users.objects.create_user(first_name=username,password=request.POST.get('password'),username=request.POST.get('phone'),phone=request.POST.get('phone'))
            form.errors['phone'] = "注册成功"
            return render(request, 'front/login.html', {'form': form })
        return render(request, 'front/login.html', {'form': form })
    else:
        form = RegisterForm()
        return render(request,'front/login.html',locals())

def userlogin(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        autologin = request.POST.get('cooketime')
        user = authenticate(request, username=phone, password=password)
        if user:
            if autologin:
                user.autologin = 1
                user.save()
            login(request, user)
            request.session.set_expiry(0)
            return redirect(reverse('front:index'))
        else:
            forms = LoginForm(request.POST)
            forms.errors['phone']='用户名或密码错误'
            return render(request,'front/login.html',locals())
    return render(request,'front/login.html',locals())
# 退出
def logoutuser(request):
    # catory = Section.objects.filter(grade=0)
    # small = Section.objects.filter(grade__gt=0)
    # man = Section.objects.get(sname='男装')
    # woman = Section.objects.get(sname='女装')
    logout(request)
    return redirect(reverse('front:index'))


def index(request):
    catory = Section.objects.filter(grade=0)
    small = Section.objects.filter(grade__gt=0)
    return render(request,'front/index.html',locals())


def section(request,sid):

    return render(request,'front/item_category.html')

# 用户信息
LOGIN_URL = '/userlogin/'
@login_required(login_url='/userlogin')
def udaisetting(request):
    if request.method == 'POST':
        if request.POST.get('基本信息'):
            print(request.POST)
            users = Users.objects.get(pk=request.user.pk)
            if request.POST. get('firstname') != '':
                users.first_name = request.POST.get('firstname')
            if request.POST.get('birthday') != 'None':
                users.birthday = request.POST.get('birthday')
            users.sex=request.POST.get('sex')
            users.save()
            return redirect(reverse('front:udaisetting'))
        elif request.POST.get('修改头像'):
            if request.FILES.get('photo') != None:
                file_obj = request.FILES.get('photo')
                obj = FileUpload(file_obj, is_randomname=True)
                path = MDEIA_ROOT
                if obj.upload(path) > 0:
                    users = Users.objects.get(pk=request.user.pk)
                    users.touxiang = '/static/upload/' + str(obj.file_name)
                    users.save()
                    return redirect(reverse('front:udaisetting'))
                else:
                    return redirect(reverse('front:udaisetting'))
            else:
                return render(request, 'front/udai_setting.html', context={
                    'alert': '请先上传文件',
                })
    return render(request,'front/udai_setting.html',locals())


def address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = Address()
            address.conname =request.POST.get('conname')
            address.telephone = request.POST.get('telephone')
            if request.POST.get('default') == 'on':
                address.is_default = 1
            address.uid = request.user
            if request.POST.get('city'):
                city = request.POST.get('city')
            else:
                city = ''
            address.address = request.POST.get('province')+city+request.POST.get('area')+request.POST.get('town')
            address.particulars = request.POST.get('particulars')
            address.save()
            return redirect(reverse('front:address'))
        else:
            return render(request, 'front/udai_address.html', {'form': form })
    else:
        address = Address.objects.filter(uid=request.user).all()
        form = AddressForm()
        return render(request,'front/udai_address.html',locals())


def edit(request,aid):
    address = Address.objects.get(id=aid)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address.conname = request.POST.get('conname')
            address.telephone = request.POST.get('telephone')
            address.uid = request.user
            if request.POST.get('city'):
                city = request.POST.get('city')
            else:
                city = ''
            address.address = request.POST.get('province') + city + request.POST.get(
                'area') + request.POST.get('town')
            address.particulars = request.POST.get('particulars')
            address.save()
            return redirect(reverse('front:address'))
        else:
            return render(request, 'front/udai_address_edit.html', {'form': form })
    if request.GET.get('isdel') == '1':
        address.delete()
        return redirect(reverse('front:address'))
    else:
        form = AddressForm()
        return render(request,'front/udai_address_edit.html',locals())

def welcome(request):
    o_all = Order.objects.filter(uid=request.user,is_back=0).order_by('-id')
    # 待支付
    o_pay = Order.objects.filter(uid=request.user,is_payment=0,is_back=0)
    # 待收货
    o_take = Order.objects.filter(uid=request.user,is_take=0,is_status=1,is_back=0)
    # 待发货
    o_sta = Order.objects.filter(uid=request.user, is_status=0,is_back=0)
    return render(request,'front/udai_welcome.html',locals())

# 订单
def order(request):
    # 全部
    order_all = Order.objects.filter(uid=request.user).order_by('-id')
    # 待支付
    order_payment = Order.objects.filter(uid=request.user,is_payment=0,is_back=0)
    # 待收货
    order_take = Order.objects.filter(uid=request.user,is_take=0,is_status=1,is_back=0)
    # 待发货
    order_status = Order.objects.filter(uid=request.user, is_status=0,is_back=0)
    return render(request,'front/udai_order.html',locals())

# 订单详情
def orderdetail(request,oid):
    orders = Order.objects.get(pk=oid)
    # 总价
    money = float(orders.cid.price)*int(orders.number)
    return render(request,'front/udai_order_detail.html',locals())


def parment(request,oid):
    orders = Order.objects.get(pk=oid)
    if request.method == 'POST':

        print(request.POST)
        add = request.POST.get('addr').split('-')
        orders.is_payment = 1
        orders.order_address = add[0]
        orders.shouname = add[1]
        orders.shouphone = add[2]
        orders.payment_time = datetime.datetime.now()
        orders.save()
        return redirect(reverse('front:userorder'))

    addre = Address.objects.filter(uid=orders.uid)
    money = orders.cid.price * int(orders.number)
    return render(request,'front/udai_shopcart_pay.html',locals())