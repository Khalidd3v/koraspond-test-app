from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("main-category", views.CategoryView.as_view(), name="main_category"),
    path("sub-category", views.SubCategoryView.as_view(), name="sub_category"),
    path("add-product", views.ProductUploadView.as_view(), name="add_product"),
]
