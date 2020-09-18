from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
import json
from .models import *


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


def product_list(request):
    products = Product.objects.all()

    if request.method == 'GET' and 'search' in request.GET:
        products = products.filter(name__contains=request.GET['search'])
    return JsonResponse({'products': [product.to_dict() for product in products]}, status=200)


def product_info(request, product_id):
    try:
        res = Product.objects.get(id=product_id)
        return JsonResponse(res.to_dict(), status=200)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Product Not Found."}, status=404)