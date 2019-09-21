from random import randint

from alipay import AliPay
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from ClothingStore.settings import MDEIA_ROOT, APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from front.form import RegisterForm, LoginForm, AddressForm
from front.models import *
from front.serializers import ShopSerializer
from tools.fileupload import FileUpload
from tools.uploads import uploads


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
                    users.touxiang = 'https://upload-1259695184.cos.ap-beijing.myqcloud.com/' + str(obj.file_name)
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
    o_all = Order.objects.filter(uid=request.user).order_by('-id')
    # 待支付
    o_pay = Order.objects.filter(uid=request.user,is_payment=0,is_back=0).order_by('-id')
    # 待收货
    o_take = Order.objects.filter(uid=request.user,is_take=0,is_status=1,is_back=0,is_payment=1).order_by('-id')
    # 待发货
    o_sta = Order.objects.filter(uid=request.user, is_status=0,is_back=0,is_payment=1,is_take=0).order_by('-id')
    return render(request,'front/udai_welcome.html',locals())

# 订单
@login_required(login_url='/userlogin')
def order(request):
    # 全部
    order_all = Order.objects.filter(uid=request.user).order_by('is_take','-id')
    # 待支付
    order_payment = Order.objects.filter(uid=request.user,is_payment=0,is_back=0,is_take=0).order_by('-id')
    # 待收货
    order_take = Order.objects.filter(uid=request.user,is_take=0,is_status=1,is_back=0,is_payment=1).order_by('-id')
    # 待发货
    order_status = Order.objects.filter(uid=request.user, is_status=0,is_back=0,is_payment=1,is_take=0).order_by('-id')
    # 已收货
    order_yes = Order.objects.filter(uid=request.user,is_take=1,is_status=1,is_back=0,is_payment=1).order_by('-id')
    return render(request,'front/udai_order.html',locals())

# 订单详情
def orderdetail(request,oid):
    orders = Order.objects.get(pk=oid)
    # 总价
    money = float(orders.cid.price)*int(orders.number)
    return render(request,'front/udai_order_detail.html',locals())


# 付款
def parment(request,oid):
    orders = Order.objects.get(pk=oid)
    if request.method == 'POST':
        add = request.POST.get('addr').split('-')
        orders.order_address = add[0]
        orders.shouname = add[1]
        orders.shouphone = add[2]
        orders.save()
        alipay = AliPay(
            appid=APPID,
            app_notify_url=None,
            app_private_key_string=APP_PRIVATE_KEY,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,
            sign_type="RSA2",
            debug=False
        )
        # 获取价格
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=orders.ordernumber,
            total_amount=orders.number*orders.cid.price,
            subject=orders.cid.cname,
            return_url="http://10.0.104.73:9000/yesorder/{}/".format(orders.id),
            notify_url="http://localhost:8000/",
        )
        net = "https://openapi.alipaydev.com/gateway.do?{}".format(order_string)
        return redirect(net)

    if request.GET.get('del') == '1':
        orders.delete()
        return redirect(reverse('front:userorder'))

    addre = Address.objects.filter(uid=orders.uid)
    money = orders.cid.price * int(orders.number)
    return render(request,'front/udai_shopcart_pay.html',locals())

# 收货
def shouhuo(request,oid):
    orders = Order.objects.get(pk=oid)
    money = int(orders.number)* orders.cid.price
    if request.method == 'POST':
        orders.is_take = 1
        orders.save()
        return redirect(reverse('front:userorder'))
    return render(request,'front/udai_order_receipted.html',locals())

# 退货
def ordertui(request,oid=None):
    # 查看
    if request.GET.get('cha') == '1':
        returnsale = SalesReturn.objects.filter(uid=request.user)
        yes_return = SalesReturn.objects.filter(uid=request.user,state__gt=0)
        no_return = SalesReturn.objects.filter(uid=request.user,state=0)
        if request.GET.get('cancel') == 'yes':
            salert = SalesReturn.objects.get(oid=oid)
            salert.delete()
            order = Order.objects.get(id=oid)
            order.is_back = 0
            order.save()
        return render(request, 'front/udai_refund.html',locals())
    # 提交
    orders = Order.objects.get(pk=oid)
    if request.method == 'POST':
        orders.is_back = 1
        orders.save()
        sales = SalesReturn()
        # 退款单
        sales.uid = orders.uid
        sales.remark = request.POST.get('remark')
        sales.cause = request.POST.get('town')
        sales.oid = orders
        sales.requesttype = request.POST.get('money')
        sales.requesttime = datetime.datetime.now()
        sales.requestcode ='TH'+str(randint(1000000000000,9999999999999))
        sales.save()
        return render(request,'front/return_yes.html')
    # 申请页面
    if request.GET.get('shen') == '1':

        return render(request,'front/udai_apply_return.html',locals())


def yesorder(request,oid):
    orders = Order.objects.get(pk=oid)
    orders.is_payment = 1
    orders.payment_time = datetime.datetime.now()
    orders.save()
    return render(request,'front/yesorder.html')

# 服装列表
def clothlist(request):
    if request.POST.get('cid'):
        add_shop = ShopCat()
        add_shop.cid = Clothing.objects.get(cid=request.POST.get('cid'))
        add_shop.uid = request.user
        add_shop.money = Clothing.objects.get(cid=request.POST.get('cid')).price
        add_shop.save()
    catory = Section.objects.filter(grade=0)
    big = Section.objects.get(sname=request.GET.get('bcategory'))
    if request.GET.get('scategory') != '全部':
        smas = Section.objects.get(sname=request.GET.get('scategory'))
    small = Section.objects.filter(grade=big.pk)
    if request.GET.get('scategory') == '全部':
        cloth = Clothing.objects.filter(sid__grade=big.pk,is_del=0)
    else:
        cloth = Clothing.objects.filter(sid__sname=request.GET.get('scategory'),is_del=0)
    requ = request.GET.get('scategory')
    return render(request,'front/item_category.html',locals())
# 购物车
@login_required(login_url='/userlogin')
def shopcat(request):
    if request.method == 'POST':
        for loop in request.POST.getlist('cid'):
            loops = loop.split('-')[-1]
            order = Order()
            order.number = request.POST.getlist('number')[int(loops)]
            order.ordernumber = 'CS'+str(randint(10000000,99999999))
            order.creation_time = datetime.datetime.now()
            order.cid = ShopCat.objects.get(id=loop.split('-')[0]).cid
            order.uid = ShopCat.objects.get(id=int(loop.split('-')[0])).uid
            order.save()
            shopdelete = ShopCat.objects.get(id=int(loop.split('-')[0]))
            shopdelete.delete()
        return redirect(reverse('front:userorder'))
    if request.GET.get('del'):
        shopdelete = ShopCat.objects.get(id=request.GET.get('del'))
        shopdelete.delete()
        return redirect('front:shopcat')
    return render(request,'front/udai_shopcart.html',locals())


# 服装详情
def clodetail(request,cid):
    catory = Section.objects.filter(grade=0)
    cloth = Clothing.objects.get(cid=cid)
    color = cloth.color.split('|')
    size = cloth.size.split('|')
    return render(request,'front/item_show.html',locals())