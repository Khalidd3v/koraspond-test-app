from django import forms
from .models import Category, SubCategory, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'required': 'true', 'placeholder' : 'Add main category'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'required': 'true', 'placeholder' : 'Add main category'}),
        }

class ProductUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File', widget=forms.FileInput(attrs={'class': 'form-control'}))
    main_category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select Main Category', widget=forms.Select(attrs={'class': 'form-control'}))
    sub_category = forms.ModelChoiceField(queryset=SubCategory.objects.all(), empty_label='Select Subcategory', widget=forms.Select(attrs={'class': 'form-control'}))
