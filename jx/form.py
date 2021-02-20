# coding=utf-8

from django import forms


class LoginForm(forms.Form):
    payroll = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "用户名"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': "密码"}
        )
    )


class RoleForm(forms.Form):
    role_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "角色名称",
                'name': "txt_department_name",
                'id': "txt_department_name"
            }
        )
    )
