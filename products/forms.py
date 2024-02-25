from django.forms import ModelForm
from django import forms
from .models import Catagory, Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "catagory", "purchase_price", "price", "unit","manufacture_date", "shelf_life", "shelf_life_unit", "expire_date", "picture", "remark"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "商品名称"
            }),
            "manufacture_date": forms.DateInput(attrs={
                "type":"date",
            }),
            "expire_date": forms.DateInput(attrs={
                "type":"date",
            }),
        }