from django.urls import path
from .views import *

app_name = 'market'
urlpatterns = [
    path('market/products/insert/', product_insert, name='product_insert'),
    path('market/products/list/', product_list, name='product_list'),
    path('market/products/<int:product_id>/', product_info, name='product_info'),
    path('market/products/<int:product_id>/edit_inventory', product_editInventory, name='product_editInventory'),
]
