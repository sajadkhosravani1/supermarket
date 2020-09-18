from django.urls import path
from .views import *

app_name = 'market'
urlpatterns = [
    path('market/product/insert/', product_insert, name='product_insert'),
    path('market/product/list/', product_list, name='product_list'),
    path('market/product/<int:product_id>/', product_info, name='product_info'),
    path('market/product/<int:product_id>/edit_inventory/', product_editInventory, name='product_editInventory'),

    path('accounts/customer/register/', customer_register, name='customer_register'),
    path('accounts/customer/list/', customer_list, name='customer_list')
]
