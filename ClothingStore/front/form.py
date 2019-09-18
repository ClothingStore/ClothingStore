import re

from django import forms
from django.core.exceptions import ValidationError



# def check_password(password):
#     if re.search(r'\d',password) and \
#        re.search(r'[a-z]',password) and  \
#        re.search(r'[A-Z]',password) and  \
#        re.search(r'[^0-9a-zA-Z]',password): \
#         return password
#     raise ValidationError('密码强度不满足要求')
from front.models import Users

def check_phone(phone):
    if re.search(r'\d',phone):
        return phone
    raise ValidationError('手机号必须为纯数字')


class RegisterForm(forms.Form):
    password = forms.CharField(label='密码',
                               max_length=12,
                               min_length=6,
                               widget=forms.PasswordInput(attrs={
                                   'placehold':'请输入密码',
                                   'class':'hahaha'
                               }),
                               # validators=[check_password],
                               error_messages={
                                   'max_length': '密码最大长度是12字符',
                                   'min_length': '密码长度不能小于6个字符',
                                   'required': '密码必须输入'
                               })
    phone = forms.CharField(label='手机号',
                               max_length=11,
                                min_length=11,
                               widget=forms.PasswordInput(attrs={
                                   'placehold': '请输入手机号',
                                   'class': 'hahaha'
                               }),
                               validators=[check_phone],
                               error_messages={
                                   'max_length': '手机号必须为11个字符',
                                   'min_length': '手机号必须为11个字符',
                                   'required': '手机号必须输入'
                               })
    def clean_phone(self):
        res = Users.objects.filter(username=self.cleaned_data.get('phone')).exists()
        if res:
            raise ValidationError("该手机号已被注册")
        return self.cleaned_data.get('phone')

class LoginForm(forms.Form):
    password = forms.CharField(label='密码')
    phone = forms.CharField(label='手机号')

class AddressForm(forms.Form):
    conname = forms.CharField(label='收件人',

                               widget=forms.PasswordInput(attrs={
                                   'placehold':'请输入',
                                   'class':'hahaha'
                               }),
                               error_messages={
                                   'required': '收件人不能为空'
                               })
    telephone = forms.CharField(label='手机号',
                               max_length=11,
                                min_length=11,
                               widget=forms.PasswordInput(attrs={
                                   'placehold': '请输入手机号',
                                   'class': 'hahaha'
                               }),
                               validators=[check_phone],
                               error_messages={
                                   'max_length': '手机号必须为11个字符',
                                   'min_length': '手机号必须为11个字符',
                                   'required': '手机号不能为空'
                               })
    particulars = forms.CharField(label='详细地址',
                               widget=forms.PasswordInput(attrs={
                                   'placehold': '请输入地址',
                                   'class': 'hahaha'
                               }),
                               error_messages={
                                   'required': '详细地址不能为空'
                               })



