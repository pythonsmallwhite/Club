# coding=gbk
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.hashers import check_password as auth_check_password  # ������ݿ����������ʵ����������


# �û�ע��
class RegisterForm(forms.Form):
    username = forms.CharField(label='�û���', required=True, min_length=3, max_length=12,
                               error_messages={'max_length': '�û���̫����', 'min_length': '�û���̫����', 'required': '�û�������Ϊ��'},
                               widget=widgets.TextInput(attrs={
                                   'class': "form-control", 'id': 'u', 'type': "text", 'placeholder': "�û���*",
                                   'name': "user",
                                   'style': "width: 520px"
                               }))
    email = forms.EmailField(label='����', required=True, error_messages={'required': '���䲻��Ϊ��', 'invalid': '�����ʽ����'},
                             widget=widgets.EmailInput(
                                 attrs={
                                     'class': "form-control", 'id': 'em', 'type': "email", 'placeholder': "����*",
                                     'name': "email",
                                     'style': "width: 520px"
                                 }
                             ))

    password = forms.CharField(label="�� ��2",min_length=6, required=True, error_messages={'min_length': '����̫����','required': '���벻��Ϊ��'},
                               widget=widgets.PasswordInput(attrs={
                                   'class': "form-control", 'id': 'p1', 'type': "password", 'placeholder': "����*",
                                   'name': "p",
                                   'style': "width: 520px"
                               }))
    password2 = forms.CharField(label="�� ��2", required=True, error_messages={'required': '���벻��Ϊ��'},
                                widget=widgets.PasswordInput(attrs={
                                    'class': "form-control", 'id': 'p2', 'type': "password", 'placeholder': "ȷ������*",
                                    'name': "p2", 'style': "width: 520px"
                                }))
    mobile = forms.CharField(label='�ֻ���', required=True, error_messages={'required': '�ֻ��Ų���Ϊ��'},
                             widget=widgets.TextInput(attrs={
                                 'class': "form-control", 'id': 'pho', 'type': "text", 'placeholder': "�ֻ���*",
                                 'name': "m",
                                 'style': "width: 520px"
                             }))
    mobile_captcha = forms.CharField(label="��֤��", required=True, error_messages={'required': '�ֻ���֤�벻��Ϊ��'},
                                     widget=widgets.TextInput(attrs={
                                         'class': "form-control", 'id': 'mc', 'type': "text", 'placeholder': "��֤��*",
                                         'name': "mc",
                                         'style': "width: 520px", }))

    # username�Ƿ��ظ�django���Զ���飬��Ϊ����unique�ģ����Բ���Ҫ�Լ�дclean_username

    def clean_mobile(self):
        ret = User.objects.filter(mobile=self.cleaned_data.get("mobile"))
        if not ret:
            return self.cleaned_data.get("mobile")
        else:
            raise ValidationError("�ֻ����Ѱ�")

    def clean_password(self):
        data = self.cleaned_data.get("password")
        if not data.isdigit():
            return self.cleaned_data.get("password")
        else:
            if len(data) == 0:
                raise ValidationError("���벻��Ϊ��")
            else:
                raise ValidationError("���벻��ȫ������")

    def clean(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("password2"):
            return self.cleaned_data
        else:
            raise ValidationError("�������벻һ��")


class LoginForm(forms.Form):
    username = forms.CharField(label='�û���', required=True, min_length=3, max_length=12,
                               error_messages={'max_length': '�û���̫����', 'min_length': '�û���̫����', 'required': '�û�������Ϊ��'},
                               widget=widgets.TextInput(attrs={
                                   'class': "form-control", 'id': 'u', 'type': "text", 'placeholder': "�û���*",
                                   'name': "user",
                                   'style': "width: 520px"
                               }))

    password = forms.CharField(label="�� ��",required=True,error_messages={ 'required': '���벻��Ϊ��'},widget=widgets.PasswordInput(
                                   attrs={'class': "form-control", 'style': "width: 520px", "placeholder": "����������*",
                                          'type': "password", 'id': 'p5', }))
    captcha = forms.CharField(label="��֤��",required=True,error_messages={'required': '��֤�벻��Ϊ��'}, widget=widgets.TextInput(
        attrs={'class': "form-control", "placeholder": "��֤��*", "onblur": "check_captcha()", 'style': "width: 520px",
               'id': 'cat', }))

    def check_password(self):
        # print('check password')
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(username=username)

            return user, auth_check_password(password, user.password)
        except:
            return None, False
    #
    # def clean_username(self):
    #     # print('hahaha')
    #     # print(self.cleaned_data.get("username"))
    #     ret = User.objects.filter(username=self.cleaned_data.get("username"))
    #     if ret:
    #         return self.cleaned_data.get("username")
    #     else:
    #         raise ValidationError("�û��������벻��ȷ")
