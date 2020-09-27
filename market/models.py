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
    balance = models.PositiveIntegerField(default=20000, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    def deposit(self, amount: int):
        """ Charges user's balance by <amount> Tomans.
        :param amount:int
        :return:void
        """
        self.balance += amount
        pass

    def spent(self, amount: int):
        """ Decreases user's balance by <amount> Tomans.
        :param amount:int
        :return:void
        """
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise Exception("Customer balance is not enough!")
        pass

    def __str__(self):
        return "Customer{address:%s, balance:%i, phone:%s, user:%s}"\
            % (self.address, self.balance, self.phone, str(self.user))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "phone": self.phone,
            "address": self.address,
            "balance": self.balance
        }


class Product(models.Model):
    """Contains products info
    code : A 10-letters word representing primary key.
    name : A string representing products name. Less than 100 chars.
    price : Price (in Tomans) of one unite of product.
    inventory : positive int - representing count of remained product.
    """
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField(default=0, null=True)

    def increase_inventory(self, amount: int):
        """ increases inventory by count of <amount>
        :param amount:int
        :return:void
        """
        if amount < 1:
            raise Exception('Invalid input.')
        self.inventory += amount
        self.save()
        pass

    def decrease_inventory(self, amount: int):
        """ decreases inventory by count of <amount>
        :param amount: positive int
        :return:void
        """
        if amount < 1:
            raise Exception('Invalid input.')
        if self.inventory >= amount:
            self.inventory -= amount
            self.save()
        else:
            raise Exception("Product inventory is not enough.")
        pass

    def to_dict(self):
        return {'id': self.id, 'code': self.code, 'name': self.name,
                'price': self.price, 'inventory': self.inventory}

    def __str__(self):
        return "Product{code:%s, name:%s, price:%i, inventory:%i}"\
               % (self.code, self.name, self.price, self.inventory)


class Order(models.Model):
    """Contains orders info
    customer : int - A integer referring to order's owner "Customer" object.
    order_time : datetime - A time object representing order time.
    total_price = positive int - referring to total
    status = A specific integer (selected from class's constants) representing order's status.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    total_price = models.IntegerField()

    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4
    status_choices = (
        (STATUS_SHOPPING, "shopping"),
        (STATUS_SUBMITTED, "submitted"),
        (STATUS_CANCELED, "canceled"),
        (STATUS_SENT, "sent"),
    )
    status = models.IntegerField(choices=status_choices)

    @staticmethod
    def initiate(customer: Customer):
        """
        initiates and returns a new order
        :param customer:Customer
        :return:Order
        """
        from django.utils import timezone
        if Order.STATUS_SHOPPING in [item.status for item in Order.objects.filter(customer=customer)]:
            return Order.objects.filter(status=Order.STATUS_SHOPPING).get(customer=customer)

        order = Order(customer=customer,
                      status=Order.STATUS_SHOPPING,
                      order_time=timezone.now(), total_price=0)
        order.save()
        order.getRows()
        return order
        pass

    def add_product(self, product: Product, amount: int):
        """Adds <amount> number of <product> into order card.
        :param product:Product
        :param amount:int
        :return:void
        """
        if amount <= 0:
            raise Exception("Wrong operation.")
        if amount > Product.objects.get(code=product.code).inventory:
            raise Exception("Inventory is not enough.")
        if product.code in [item.product.code for item in self.getRows()]:
            order_row = self.getOrderRow(product)
            order_row.amount += amount
            if order_row.amount > Product.objects.get(code=product.code).inventory:
                raise Exception("Inventory is not enough.")
            order_row.save()
        else:
            order_row = OrderRow(product=product, amount=amount, order=self)
            order_row.save()

        from django.utils import timezone
        self.order_time = timezone.now()
        self.total_price += product.price * amount
        self.save()
        pass

    def remove_product(self, product: Product, amount: int = None):
        """Removes <amount> number of <product>s existing in order card.
        If amount would not be given all the <product>s will be removed.
        :param product:Product
        :param amount:int Optional
        :return:void
        """
        if amount and amount <= 0 or not Product.objects.filter(code=product.code).exists():
            raise Exception("Wrong operation.")

        if product.code in [item.product.code for item in self.getRows()]:
            order_row = self.getOrderRow(product)
            if amount is None or order_row.amount == amount:
                order_row.delete()
                self.total_price -= product.price * order_row.amount
            elif order_row.amount > amount:
                order_row.amount -= amount
                self.total_price -= product.price * amount
                order_row.save()
            else:
                raise Exception("Entered amount is much than the amount in the card.")

        else:
            raise Exception("There is no such product in customer's card.")

        from django.utils import timezone
        self.order_time = timezone.now()
        self.save()

        pass

    def submit(self):
        """Saves the order and turn's order status to STATUS_SHOPPING
        if enough amount of ordered products could be satisfied.
        :return:void
        """

        #       validation

        # It's better to reduce product's inventories before validating inorder
        # to prevent conflict between the shopping.
        # If the submit was not success full the inventories will be increased by the decreased value.

        if self.status != Order.STATUS_SHOPPING:
            raise Exception("This order is not submittable.")
        if len(self.getRows()) == 0:
            raise Exception("The cart is empty.")

        temporarily_reduced = dict()

        def recharge_inventories(max_):
            """Increases inventories by reduced value, for all of manipulated products.
            :param max_:int last index of manipulated products in orderRows list. #exlusive!"""
            for order_row_ in self.getRows():
                order_row_.product.increase_inventory(temporarily_reduced[order_row_.id])

        i = 0
        for order_row in self.getRows():
            if order_row.amount > order_row.product.inventory:
                recharge_inventories(i)
                raise Exception(
                    """The product \"%s\" has been bought by other customers while you where shopping. 
                    Now the product's inventory is %i numbers.""" \
                    % (order_row.product.name, order_row.product.inventory))
            else:
                temporarily_reduced[order_row.id] = order_row.amount
                order_row.product.decrease_inventory(order_row.amount)
            i += 1


        price_sum = sum([item.product.price * item.amount for item in self.getRows()])
        customer_balance = self.customer.balance
        if price_sum > customer_balance:
            recharge_inventories(i)
            raise Exception("Not enough balance.")

        #       submit
        self.customer.balance -= price_sum
        self.customer.save()
        self.status = Order.STATUS_SUBMITTED
        from django.utils import timezone
        self.order_time = timezone.now()
        self.save()
        pass

    def cancel(self):
        """Cancels the order (if is submitted) and gives back the customers charge.
        Gives back ordered product's to products inventory.
        And changes order status to STATUS_CANCELED
        :return:void
        """
        if self.status != Order.STATUS_SUBMITTED:
            raise Exception("Not permitted operation.")

        if self.status == Order.STATUS_SUBMITTED:
            for order_row in self.getRows():
                self.customer.balance += order_row.product.price * order_row.amount
                self.customer.save()
                order_row.product.increase_inventory(order_row.amount)

        self.status = Order.STATUS_CANCELED
        self.save()
        pass

    def send(self):
        """Changes order's status from STATUS_SUBMITTED to STATUS_SENT
        :return:void"""
        if self.status != Order.STATUS_SUBMITTED:
            raise Exception("The order is not submitted or has been cancelled.")
        self.status = Order.STATUS_SENT
        self.save()
        pass

    def getOrderRow(self, product: Product):
        return self.orderrow_set.get(product=product)

    def __str__(self):
        dic = dict(Order.status_choices)
        return "Order{customer:%s, order_time:%s, rows:%s, status:%s, total_price:%i}"\
            % (str(self.customer), str(self.order_time), str(self.getRows()), dic[self.status], self.total_price)

    def to_dict(self, errors=None):
        out = {
            'total_price': self.total_price,
            'items': [item.to_dict() for item in OrderRow.objects.filter(order=self.id)]
        }
        if errors:
            out['errors'] = errors
        return out

    def toDict(self):
        return {
            'id': self.id,
            'order_time': self.order_time.strftime("%Y-%m-%d %H:%M:%S"),
            'status': dict(Order.status_choices)[self.status],
            'total_price': self.total_price,
            'rows': [item.to_dict() for item in self.getRows()]
        }

    def getRows(self):
        self.rows = list(self.orderrow_set.all())
        return self.rows


class OrderRow(models.Model):
    """Represents orders one single item.
    product : int - foreign key referring to Product.
    amount : positive int - count of ordered products.
    order : Order - foreign key referring to parent order
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return "OrderRow{product:%s, amount: %i}"\
               % (str(self.product), self.amount)

    def to_dict(self):
        return {
            'code': self.product.code,
            'name': self.product.name,
            'price': self.product.price,
            'amount': self.amount
        }