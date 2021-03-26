from django.contrib.auth import authenticate
from django import forms
from django.forms import widgets
from .models import User, Product, ProductIncome, ProductSell


class SignInForm(forms.Form):
    username = forms.CharField(label='Email', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Invalid username or password')


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'base_wallet','username', 'first_name', 'last_name']
        widgets = {
            'password': widgets.PasswordInput
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']


class ProductIncomeForm(forms.ModelForm):
    class Meta:
        model = ProductIncome
        fields = ['product', 'quantity']


class ProductSellForm(forms.ModelForm):
    class Meta:
        model = ProductSell
        fields = ['quantity']

