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
        form = ProductUploadForm()
        return render(request, 'app/products.html', {'form': form})

    def post(self, request):
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            main_category = form.cleaned_data['main_category']
            sub_category = form.cleaned_data['sub_category']

            try:
                # Read CSV file using pandas
                df = pd.read_csv(csv_file)
                print(df.columns.tolist())
                # Assuming CSV format: name, size, color, price, brand, quantity, extra_field_key1, extra_field_value1, extra_field_key2, extra_field_value2, ...
                for index, row in df.iterrows():
                    pass
                    # product_data = {
                    #     'name': row['name'],
                    #     'size': row['size'],
                    #     'color': row['color'],
                    #     'price': row['price'],
                    #     'brand': row['brand'],
                    #     'quantity': row['quantity'],
                    #     'category': main_category,
                    #     'sub_category': sub_category,
                    # }
                    # Extract extra fields if any
                    # extra_fields = {}
                    # for column in df.columns[6:]:
                    #     extra_fields[column] = row[column]
                    # if extra_fields:
                    #     product_data['extra_fields'] = json.dumps(extra_fields)
                    # Product.objects.create(**product_data)
                
                messages.success(request, 'Products uploaded successfully!')
                return redirect('add_product')
            except Exception as e:
                print(e)
                messages.error(request, 'Error processing CSV file. Please try again.')
        else:
            messages.error(request, form.errors)
        
        return render(request, 'app/products.html', {'form': form})
