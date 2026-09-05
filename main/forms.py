from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'sku', 'price', 'stock_quantity', 'size', 'color', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Premium Cotton T-Shirt'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Soft cotton T-shirt...'}),
            'sku': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'TS-BLK-XL'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '700.00'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '25'}),
            'size': forms.Select(attrs={'class': 'form-input'}),
            'color': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Black'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
        }