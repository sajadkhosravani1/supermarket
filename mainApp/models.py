from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.IntegerField()
    user = models.OneToOneField(User,on_delete=models.CASCADE,)


class Product(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    inventory = models.IntegerField()


# TODO : Product class


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    total_price = models.IntegerField()
    status = models.IntegerField()  # TODO : choices for status
    # TODO : rows



# TODO : OrderRow class
