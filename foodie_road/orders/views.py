import json
from orders.models import Order
from stores.models import StoreMenu, Store, StoreImage
from cores.utils import signin_decorator

from django.views import View
from django.http  import JsonResponse

class OrderView(View):
    @signin_decorator
    def get(self,request):
        try : 
            orders = Order.objects.filter(user_id = request.user.id)
            result = []
            for order in orders:
                store_id = Store.objects.get(id = order.store_id).id
                store_image = StoreImage.objects.get(store_id = store_id)
                result.append({
                        "order_id" : order.id,
                        "store_id" : order.store_id,
                        "price" : order.price,
                        "store_thumnail" : store_image.image_urls
                    })
            return JsonResponse({'orders' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status = 400) 
    
    @signin_decorator
    def post(self,request):
        try :
            data = json.loads(request.body)
            menu_list = data['menu']
            store_id = data['store_id']
            price = 0

            for menu_id in menu_list:
                menu = StoreMenu.objects.get(id = menu_id)
                price = price + menu.menu_price
            Order.objects.create(  
                user_id = request.user.id,
                store_id = store_id,
                menu = menu_list,
                price = price
            )
            return JsonResponse({'message' : 'order created'}, status = 201)

        except KeyError:
            return JsonResponse({'message':'KeyError'}, status = 400)   