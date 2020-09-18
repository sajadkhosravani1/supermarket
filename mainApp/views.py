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

