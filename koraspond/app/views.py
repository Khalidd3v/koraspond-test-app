from django.views import View
from django.shortcuts import render, redirect
from .forms import CategoryForm, SubCategoryForm, ProductUploadForm
from .models import Category, SubCategory, Product
from django.contrib import messages
import pandas as pd
import json

def home(request):
    return render(request, 'app/index.html')

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, 'app/main-category.html', {'categories': categories, 'form': form})

    def post(self, request):
        # category = request.POST.get('category', None)
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "New Main Category added successfully!")
                return redirect('main_category')
            except:
                messages.error(request, "Something went wrong while saving the Main Category. Please try again.")
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
        categories = Category.objects.all()
        return render(request, 'app/main-category.html', {'categories': categories, 'form': form})


class SubCategoryView(View):
    def get(self, request):
        subcategories = SubCategory.objects.all()
        form = SubCategoryForm()
        return render(request, 'app/sub-category.html', {'subcategories': subcategories, 'form': form})

    def post(self, request):
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "New Sub Category added successfully!")
                return redirect('sub_category')
            except:
                messages.error(request, "Something went wrong while saving the subcategory. Please try again.")
        else:
            messages.error(request, "Invalid form submission. Please correct the errors.")
        subcategories = SubCategory.objects.all()
        return render(request, 'app/sub-category.html', {'subcategories': subcategories, 'form': form})


class ProductUploadView(View):
    def get(self, request):
        products = Product.objects.all()
        extra_fields_keys = []
        if products:
            first_product = products[0]
            if first_product.extra_fields:
                try:
                    extra_fields = json.loads(first_product.extra_fields)
                    extra_fields_keys = list(extra_fields.keys())
                except Exception as e:
                    print(e)

        form = ProductUploadForm()
        return render(request, 'app/products.html', {'form': form, 'products': products, 'extra_fields': extra_fields_keys})

    def post(self, request):
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            main_category = form.cleaned_data['main_category']
            sub_category = form.cleaned_data['sub_category']
            try:
                if not csv_file.name.endswith('.csv'):
                    df = pd.read_excel(csv_file)
                else:
                    df = pd.read_csv(csv_file)
                column_names = df.columns.tolist()
                name_identifier = ['name', 'product_name', 'title']
                size_identifier = ['size', 'size_name']
                color_identifier = ['color', 'colour']
                price_identifier = ['price', 'cost']
                brand_identifier = ['brand', 'manufacturer']
                quantity_identifier = ['quantity', 'stock', 'stock_quantity']
                for index, row in df.iterrows():
                    for col in column_names:
                        if col in name_identifier:
                            name = row[col]
                        elif col in size_identifier:
                            size = row[col]
                        elif col in color_identifier:
                            color = row[col]
                        elif col in price_identifier:
                            price = row[col]
                        elif col in brand_identifier:
                            brand = row[col]
                        elif col in quantity_identifier:
                            quantity = row[col]

                    product_data = {
                        'name': name,
                        'size': size,
                        'color': color,
                        'price': price,
                        'brand': brand,
                        'quantity': quantity,
                        'category': main_category,
                        'sub_category': sub_category,
                    }

                    extra_fields = {}
                    for column in df.columns[6:]:
                        extra_fields[column] = row[column]
                    if extra_fields:
                        product_data['extra_fields'] = json.dumps(extra_fields)
                    Product.objects.create(**product_data)

                messages.success(request, 'Products uploaded successfully!')
                return redirect('add_product')
            except Exception as e:
                print(e)
                messages.error(request, 'Error processing CSV file. Please try again.')
        else:
            messages.error(request, form.errors)
        
        return redirect('add_product')