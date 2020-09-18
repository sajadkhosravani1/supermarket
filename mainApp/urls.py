from django.urls import path
from .views import *

app_name = 'market'
urlpatterns = [
    path('products/insert/', product_insert, name='product_insert'),
    path('products/list/', product_list, name='product_list')
]
