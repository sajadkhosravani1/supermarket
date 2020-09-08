from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """Represents market related data of Customers
    phone : a string representing phone number
    address : home address
    balance : positive int - representing users balance by Toman units.
     each user receives 20000 as registers.
    user : related django user
    """
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    def deposit(self, amount: int):
        """ Charges user's balance by <amount> Tomans.
        :param amount:int
        :return:void
        """
        pass

    def spent(self, amount: int):
        """ Decreases user's balance by <amount> Tomans.
        :param amount:int
        :return:void
        """
        pass


class Product(models.Model):
    """Contains products info
    code : A 10-letters word representing primary key.
    name : A string representing products name. Less than 100 chars.
    inventory : positive int - representing count of remained product.
    """
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    inventory = models.IntegerField()

    def increase_inventory(self, amount:int):
        """ increases inventory by count of <amount>
        :param amount:int
        :return:void
        """
        pass

    def decrease_inventory(self, amount:int):
        """ decreases inventory by count of <amount>
        :param amount:int
        :return:void
        """
        pass


class Order(models.Model):
    """Contains orders info
    customer : int - A integer referring to order's owner "Customer" object.
    order_time : datetime - A time object representing order time.
    total_price = positive int - referring to total
    status = A specific integer (selected from class's constants) representing order's status.
    rows = TODO
    """
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


    def initiate(self, customer):
        """
        initiates new orders.
        :param customer:Customer
        :return:void
        """
        pass

    def add_product(self, product: Product, amount:int):
        """Adds <amount> number of <product> into order card.

        :param product:Product
        :param amount:int
        :return:void
        """
        pass

    def remove_product(self, product: Product, amount: int = None):
        """Removes <amount> number of <product>s existing in order card.
        If amount would not be given all the <product>s will be removed.
        :param product:Product
        :param amount:int Optional
        :return:void
        """
        pass

    def submit(self):
        """Saves the order and turn's order status to STATUS_SHOPPING
        if enough amount of ordered products could be satisfied.
        :return:void
        """
        pass

    def cancel(self):
        """Cancels the order (if is submitted) and gives back the customers charge.
        Gives back ordered product's to products inventory.
        And changes order status to STATUS_CANCELED
        :return:void
        """
        pass

    def send(self):
        """Changes order's status from STATUS_SUBMITTED to STATUS_SENT
        :return:void"""
        pass


class OrderRow(models.Model):
    """Represents orders one single item.
    product : int - foreign key referring to Product.
    amount : positive int - count of ordered products.
    order : Order - foreign key referring to parent order
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
