from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
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
        res = ects.get(id=product_id)
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
    except Exceptoin:
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