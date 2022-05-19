from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products, name="products"),
    path('add_products/', views.add_products, name="add_products"),
    path('delete_products/<int:id>', views.delete_products, name="delete_products"),
    path('edit_products/<int:id>', views.edit_products, name="edit_products"),
]