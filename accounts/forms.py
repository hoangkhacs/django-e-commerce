from django import forms
from django.forms import CharField
from django.forms import widgets
from .models import Account


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)

    last_name = forms.CharField(max_length=100)

    phone_number = forms.CharField(max_length=50)

    email = forms.EmailField(max_length=50)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Vui lòng nhập mật khẩu', 'id' : 'password1'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Nhập lại mật khẩu', 'id' : 'password2'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Vui lòng nhập tên'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Vui lòng nhập họ'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Vui lòng nhập số diện thoại'
        self.fields['phone_number'].widget.attrs['id'] = 'phone'
        self.fields['email'].widget.attrs['placeholder'] = 'Vui lòng nhập email'
        self.fields['email'].widget.attrs['id'] = 'email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('Vui lòng nhập mật khẩu')
        confirm_password = cleaned_data.get('Nhập lại mật khẩu')

        if password != confirm_password:
            raise forms.ValidationError(
                'Mật khẩu không trùng nhau.'
            )
