from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
import json
from .models import *


# Products


@csrf_exempt
def product_insert(request):
    args = json.loads(request.body.decode('utf-8'))
    product = Product(code=args['code'], name=args['name'], price=args['price'])
    if 'inventory' in args :
        product.inventory = args['inventory']

    try:
        product.save()
    except IntegrityError:
        return JsonResponse({'message': "There's another product with this code."}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)
    return JsonResponse({'id':product.id}, status=201)


@csrf_exempt
def product_list(request):
    products = Product.objects.all()

    if request.method == 'GET' and 'search' in request.GET:
        products = products.filter(name__contains=request.GET['search'])
    return JsonResponse({'products': [product.to_dict() for product in products]}, status=200)


@csrf_exempt
def product_info(request, product_id):
    try:
        res = Product.objects.get(id=product_id)
        return JsonResponse(res.to_dict(), status=200)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Product Not Found."}, status=404)


@csrf_exempt
def product_editInventory(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Product Not Found."}, status=404)

    amount = json.loads(request.body.decode('utf-8'))['amount']
    try:
        if amount > 0:
            product.increase_inventory(amount)
        else:
            amount *= -1
            product.decrease_inventory(amount)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse(product.to_dict(), status=200)


# Customers


@csrf_exempt
def customer_register(request):
    try:
        args = json.loads(request.body.decode('utf-8'))
        user = User(username=args['username'], first_name=args['first_name'], last_name=args['last_name'],
                    email=args['email'])
        user.set_password(args['password'])
        user.save()
    except IntegrityError:
        return JsonResponse({"message": "Username already exists."}, status=400)
    except Exception:
        return JsonResponse({"message": "Something is wrong!"}, status=400)

    try:
        customer = Customer(phone=args['phone'], address=args['address'], user=user)
        customer.save()
    except Exception:
        user.delete()
        return JsonResponse({"message": "Something is wrong!"}, status=400)

    return JsonResponse({'id': customer.id}, status=201)


@csrf_exempt
def customer_list(request):
    customers = Customer.objects.all()

    if request.method == 'GET' and 'search' in request.GET:
        from django.db.models import Q
        searched = request.GET['search']
        customers = customers.filter(Q(user__first_name__contains=searched) |
                             Q(user__last_name__contains=searched) |
                             Q(user__username__contains=searched) |
                             Q(address__contains=searched))
    return JsonResponse({'products': [customer.to_dict() for customer in customers]}, status=200)


@csrf_exempt
def customer_info(request, customer_id):
    try:
        res = Customer.objects.get(id=customer_id)
        return JsonResponse(res.to_dict(), status=200)
    except Customer.DoesNotExist:
        return JsonResponse({"message": "Customer Not Found."}, status=404)


@csrf_exempt
def customer_edit(request, customer_id):
    args = json.loads(request.body.decode('utf-8'))
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({"message": "Customer Not Found."}, status=404)

    if 'username' in args or 'password' in args or 'id' in args:
        return JsonResponse({"message": "Cannot edit customer's identity and credentials."},
                            status=403)

    import copy
    user_before = copy.copy(customer.user)

    changed = False
    if 'first_name' in args:
        customer.user.first_name = args['first_name']
        changed = True
    if 'last_name' in args:
        customer.user.last_name = args['last_name']
        changed = True
    if 'email' in args:
        customer.user.email = args['email']
        changed = True

    try:
        if changed:
            customer.user.save()
    except Exception:
        return JsonResponse({"message":"Something is wrong."}, status=400)



    changed = False

    if 'address' in args:
        customer.address = args['address']
        changed = True
    if 'balance' in args:
        customer.balance = args['balance']
        changed = True
    if 'phone' in args:
        customer.phone = args['phone']
        changed = True
    try:
        if changed:
            customer.save()
    except Exception:
        user_before.save()
        return JsonResponse({"message":"Something is wrong."}, status=400)

    return JsonResponse(customer.to_dict(), status=200)


@csrf_exempt
def customer_login(request):
    try:
        args = json.loads(request.body.decode('utf-8'))
        if not request.user.is_active:
            return JsonResponse({"message": "User is deactivated."}, status=403)
        if request.user.is_authenticated:
            return JsonResponse({"message": "Already authenticated."}, status=200)
        user = authenticate(request, username=args['username'], password=args['password'])
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "You are logged in successfully."}, status=200)
        else:
            return JsonResponse({"message": "Username or Password is incorrect."}, status=404)
    except:
        return JsonResponse({"message": "Something is wrong! please read the documentations."}, status=404)


@csrf_exempt
def customer_logout(request):
    try:
        args = json.loads(request.body.decode('utf-8'))
        if request.method != "POST" or len(args) > 0:
            raise Exception("")
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"message": "You are logged out successfully."}, status=200)
        else:
            return JsonResponse({"message": "You are not logged in."}, status=403)
    except:
        return JsonResponse({"message": "Something is wrong! please read the documentations."}, status=404)


@csrf_exempt
def customer_profile(request):
    if request.user.is_authenticated:
        return JsonResponse(request.user.customer.to_dict(), status=200)
    else:
        return JsonResponse({"message": "You are not logged in."}, status=403)


# Orders

@csrf_exempt
def shopping_cart(request):
    if request.user.is_authenticated and request.user.is_active:
        from django.db.models import Q
        order = Order.objects.filter(Q(status=Order.STATUS_SHOPPING) | Q(status=Order.STATUS_SUBMITTED))\
            .get(customer=request.user.customer)
        return JsonResponse(order.to_dict(), status=200)
    else:
        return JsonResponse({"message": "You are not logged in."}, status=403)


@csrf_exempt
def shopping_add_items(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Wrong method.'}, status=404)

    try:
        if request.user.is_authenticated and request.user.is_active:
            raw_json = request.body.decode('utf-8')
            try:
                arr = json.loads(raw_json)
                if not isinstance(arr, list):
                    raise Exception()
            except:
                return JsonResponse({'message': 'Not able to read your request body.'}, status=404)

            from django.db.models import Q
            order = Order.objects.filter(Q(status=Order.STATUS_SHOPPING) | Q(status=Order.STATUS_SUBMITTED)) \
                .get(customer=request.user.customer)

            errors = []
            for item in arr:
                if 'code' in item and 'amount' not in item:
                    errors.append({'code': item['code'],
                                   'message': 'Item has no "amount" property.'})
                    continue
                if 'code' not in item:
                    errors.append({'code': '?',
                                   'message': 'Item has no "code" property.'})
                    continue

                try:
                    if Product.objects.filter(code=item['code']).exists():
                        order.add_product(Product.objects.get(code=item['code']), item['amount'])
                    else:
                        raise Exception("No such product.")
                except Exception as e:
                    errors.append({'code': item['code'], 'message': str(e)})

            if errors:
                return JsonResponse(order.to_dict(errors), status=400)
            else:
                return JsonResponse(order.to_dict(), status=200)

        else:
            return JsonResponse({"message": "You are not logged in."}, status=403)
    except Exception:
        JsonResponse({"message": "Something is wrong."}, status=404)


@csrf_exempt
def shopping_remove_items(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Wrong method.'}, status=404)
    try:
        if request.user.is_authenticated and request.user.is_active:
            raw_json = request.body.decode('utf-8')
            try:
                arr = json.loads(raw_json)
                if not isinstance(arr, list):
                    raise Exception()
            except:
                return JsonResponse({'message': 'Not able to read your request body.'}, status=404)

            from django.db.models import Q
            order = Order.objects.filter(Q(status=Order.STATUS_SHOPPING) | Q(status=Order.STATUS_SUBMITTED)) \
                .get(customer=request.user.customer)

            errors = []
            for item in arr:
                try:
                    if 'code' not in item:
                        errors.append({'code': '?',
                                       'message': 'Item has no "code" property.'})
                        continue

                    if Product.objects.filter(code=item['code']).exists():
                        if 'amount' not in item:
                            item['amount'] = None
                        order.remove_product(Product.objects.get(code=item['code']), item['amount'])
                    else:
                        raise Exception("No such product.")
                except Exception as e:
                    errors.append({'code': item['code'], 'message': str(e)})

            if errors:
                return JsonResponse(order.to_dict(errors), status=400)
            else:
                return JsonResponse(order.to_dict(), status=200)

        else:
            return JsonResponse({"message": "You are not logged in."}, status=403)
    except Exception:
        JsonResponse({"message": "Something is wrong."}, status=404)