from stores.models import Store, StoreImage, StoreMenu

from django.views import View
from django.http  import JsonResponse

class StoreListView(View):
    def get(self, request, ct_id):
        stores = Store.objects.filter(category = ct_id)\
        .prefetch_related('image').order_by('id')

        results = []
        for store in stores:
            image = StoreImage.objects.get(store_id = store.id)
            results.append({
                "storeName" : store.store_name,
                "storeId" : store.id,
                "storeImage" : image.image_urls
            })
        
        return JsonResponse({'result' : results}, status = 200)

class StoreDetailView(View):
    def get(self, request, store_id):
        store = Store.objects.get(id = store_id)
        menus = StoreMenu.objects.filter(store_id = store.id)

        results = []
        results.append({
            "storeDescription" : store.description
        })
        for menu in menus:
            results.append({
                "menuName" : menu.menu_name,
                "menuPrice" : menu.menu_price,
                "menuId": menu.id
            })

        return JsonResponse({'result' : results}, status = 200)
        