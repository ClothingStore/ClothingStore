from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    uid = models.AutoField(primary_key=True)
    # 手机号
    phone = models.CharField(max_length=12,null=True)
    # 邮箱
    email = models.CharField(max_length=200, blank=True, null=True)
    # 总购买金额
    amount = models.FileField(default=0)
    # 会员等级 与购买金额挂钩 默认为黑铁会员
    ex = models.IntegerField(default=50)
    sex = models.IntegerField(default=0)
    birthday = models.CharField(null=True,max_length=20)
    touxiang = models.CharField(null=True,max_length=200)
    # 支付密码
    payment = models.CharField(default='000000',max_length=6)
    class Meta:
        managed = True
        db_table = 'member'

class Section(models.Model):
    sid = models.AutoField(primary_key=True)
    # 版块名字
    sname = models.CharField(max_length=20,null=True)
    # 0 男装女装 1 服装类别
    grade = models.IntegerField(default=0)
    class Meta:
        managed = True
        db_table = 'section'

class Clothing(models.Model):
    cid = models.AutoField(primary_key=True)
    # 商品编号
    productID = models.CharField(max_length=12)
    # 服装名
    cname = models.CharField(max_length=64)
    # 上架时间
    data = models.DateTimeField(null=True)
    # 服装库存
    number = models.IntegerField(default=0)
    # 颜色
    color = models.CharField(default='白色|黑色',max_length=32)
    # 尺寸
    size = models.CharField(default='L|XL|M|S',max_length=32)
    # 图片
    # 服装价格
    price = models.FloatField(default=0.00)
    # 服装属于哪个版块
    sid = models.ForeignKey(Section, models.DO_NOTHING, db_column='sid', blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'clothing'

class ClothingDetail(models.Model):
    preview1 = models.CharField(max_length=255,null=True)
    preview2 = models.CharField(max_length=255, null=True)
    preview3 = models.CharField(max_length=255, null=True)
    preview4 = models.CharField(max_length=255, null=True)
    preview5 = models.CharField(max_length=255, null=True)
    # 产品图
    drawing = models.CharField(max_length=255, null=True)
    # 细节图
    detailed = models.CharField(max_length=255, null=True)
    # 模特图
    modeled = models.CharField(max_length=255, null=True)
    cid = models.OneToOneField(Clothing, models.DO_NOTHING, db_column='cid', unique=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'clothingdetail'

class ShopCat(models.Model):
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    cid = models.ForeignKey('Clothing', models.DO_NOTHING, db_column='cid', blank=True, null=True)
    # 商品数量
    number = models.IntegerField(null=True)
    # 商品总价格
    money = models.FileField(null=True)
    class Meta:
        managed = True
        db_table = 'shopcat'

class Order(models.Model):
    ordernumber = models.CharField(max_length=10,null=True)
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    cid = models.ForeignKey('Clothing', models.DO_NOTHING, db_column='cid', blank=True, null=True)
    number = models.IntegerField(null=True,default=1)
    # 0 为未发货 1 为发货
    is_status = models.IntegerField(default=0)
    # 默认为付款
    is_payment = models.IntegerField(default=0)
    # 是否收货
    is_take = models.IntegerField(default=0)
    # 默认为0 表示未退
    is_back = models.IntegerField(default=0)

    # 收货人
    shouname = models.CharField(max_length=16)
    # 收货手机号
    shouphone = models.CharField(max_length=11)
    # 送货地址
    order_address = models.CharField(max_length=255)
    # 创建时间
    creation_time = models.DateTimeField(null=True)
    # 付款时间
    payment_time = models.DateTimeField(null=True)
    class Meta:
        managed = True
        db_table = 'order'

# 限时折扣
class Discount(models.Model):
    cid = models.ForeignKey('Clothing', models.DO_NOTHING, db_column='cid', blank=True, null=True)
    money = models.FloatField(default=0.00)
    deadline = models.DateTimeField(null=True)
    class Meta:
        managed = True
        db_table = 'discount'

# 收货地址
class Address(models.Model):
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    # 收货地址
    address = models.CharField(max_length=200)
    #默认为0 为1为默认收货地址
    is_default = models.IntegerField(default=0)
    # 收货人
    conname = models.CharField(max_length=12)
    telephone = models.CharField(max_length=11)
    # 地址详情
    particulars = models.CharField(max_length=200,null=True)
    class Meta:
        managed = True
        db_table = 'address'

