from django.urls import path
from .views import *

app_name = 'market'
urlpatterns = [
    path('market/product/insert/', product_insert, name='product_insert'),
    path('market/product/list/', product_list, name='product_list'),
    path('market/product/<int:product_id>/', product_info, name='product_info'),
    path('market/product/<int:product_id>/edit_inventory/', product_editInventory, name='product_editInventory'),

    path('accounts/customer/register/', customer_register, name='customer_register'),
    path('accounts/customer/list/', customer_list, name='customer_list'),
    path('accounts/customer/<int:customer_id>/', customer_info, name='customer_info'),
    path('accounts/customer/<int:customer_id>/edit/', customer_edit, name='customer_edit'),
    path('accounts/customer/login/', customer_login, name='customer_login'),
    path('accounts/customer/logout/', customer_logout, name='customer_logout'),
    path('accounts/customer/profile/', customer_profile, name='customer_profile'),

    path('market/shopping/cart/', shopping_cart, name='shopping_cart'),
    path('market/shopping/cart/add_items/', shopping_add_items, name='shopping_add_items'),
    path('market/shopping/cart/remove_items/', shopping_remove_items, name='shopping_remove_items'),
]
