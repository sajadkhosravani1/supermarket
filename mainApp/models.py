from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    def deposit(self, amount):
        pass

    def spent(self, amount):
        pass


class Product(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    inventory = models.IntegerField()

    def increase_inventory(self, amount):
        pass

    def decrease_inventory(self, amount):
        pass


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    total_price = models.IntegerField()

    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4
    status_choices = (
        (STATUS_SHOPPING, "در حال خرید"),
        (STATUS_SUBMITTED, "ثبت‌شده"),
        (STATUS_CANCELED, "لغوشده"),
        (STATUS_SENT, "ارسال‌شده"),
    )
    status = models.IntegerField(choices=status_choices)

    # TODO : rows

    def initiate(self, customer):
        pass

    def add_product(self, product: Product):
        pass

    def remove_product(self, product: Product):
        pass

    def submit(self):
        pass

    def cancel(self):
        pass

    def send(self):
        pass


class OrderRow(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
