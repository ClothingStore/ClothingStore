# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=200)
    is_default = models.IntegerField()
    conname = models.CharField(max_length=12)
    telephone = models.CharField(max_length=11)
    particulars = models.CharField(max_length=200, blank=True, null=True)
    uid = models.ForeignKey('Member', models.DO_NOTHING, db_column='uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Clothing(models.Model):
    cid = models.AutoField(primary_key=True)
    productid = models.CharField(db_column='productID', max_length=12)  # Field name made lowercase.
    cname = models.CharField(max_length=64)
    data = models.DateTimeField(blank=True, null=True)
    number = models.IntegerField()
    color = models.CharField(max_length=32)
    size = models.CharField(max_length=32)
    price = models.FloatField()
    sid = models.ForeignKey('Section', models.DO_NOTHING, db_column='sid', blank=True, null=True)
    is_del = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clothing'


class Clothingdetail(models.Model):
    preview1 = models.CharField(max_length=255, blank=True, null=True)
    preview2 = models.CharField(max_length=255, blank=True, null=True)
    preview3 = models.CharField(max_length=255, blank=True, null=True)
    preview4 = models.CharField(max_length=255, blank=True, null=True)
    preview5 = models.CharField(max_length=255, blank=True, null=True)
    drawing = models.CharField(max_length=255, blank=True, null=True)
    detailed = models.CharField(max_length=255, blank=True, null=True)
    modeled = models.CharField(max_length=255, blank=True, null=True)
    cid = models.ForeignKey(Clothing, models.DO_NOTHING, db_column='cid', unique=True, blank=True, null=True)
    problem = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clothingdetail'


class Discount(models.Model):
    money = models.FloatField()
    deadline = models.DateTimeField(blank=True, null=True)
    cid = models.ForeignKey(Clothing, models.DO_NOTHING, db_column='cid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Member', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Member(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    uid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    amount = models.CharField(max_length=100)
    ex = models.IntegerField()
    sex = models.IntegerField()
    birthday = models.CharField(max_length=20, blank=True, null=True)
    touxiang = models.CharField(max_length=200, blank=True, null=True)
    payment = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'member'


class MemberGroups(models.Model):
    users = models.ForeignKey(Member, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'member_groups'
        unique_together = (('users', 'group'),)


class MemberUserPermissions(models.Model):
    users = models.ForeignKey(Member, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'member_user_permissions'
        unique_together = (('users', 'permission'),)


class Order(models.Model):
    creation_time = models.DateTimeField(blank=True, null=True)
    is_back = models.IntegerField(blank=True, null=True)
    order_address = models.CharField(max_length=255, blank=True, null=True)
    ordernumber = models.CharField(max_length=10, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    is_status = models.IntegerField()
    is_payment = models.IntegerField()
    is_take = models.IntegerField()
    cid = models.ForeignKey(Clothing, models.DO_NOTHING, db_column='cid', blank=True, null=True)
    uid = models.ForeignKey(Member, models.DO_NOTHING, db_column='uid', blank=True, null=True)
    payment_time = models.DateTimeField(blank=True, null=True)
    shouname = models.CharField(max_length=16, blank=True, null=True)
    shouphone = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class Salesreturn(models.Model):
    remark = models.CharField(max_length=255, blank=True, null=True)
    cause = models.CharField(max_length=32, blank=True, null=True)
    requestcode = models.CharField(max_length=16)
    requesttime = models.DateTimeField(blank=True, null=True)
    requesttype = models.IntegerField()
    state = models.IntegerField()
    oid = models.ForeignKey(Order, models.DO_NOTHING, db_column='oid', blank=True, null=True)
    uid = models.ForeignKey(Member, models.DO_NOTHING, db_column='uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salesreturn'


class Section(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=20, blank=True, null=True)
    grade = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'section'


class Shopcat(models.Model):
    number = models.IntegerField(blank=True, null=True)
    money = models.FloatField(blank=True, null=True)
    cid = models.ForeignKey(Clothing, models.DO_NOTHING, db_column='cid', blank=True, null=True)
    uid = models.ForeignKey(Member, models.DO_NOTHING, db_column='uid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shopcat'


class Superuserg(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'superuserg'
