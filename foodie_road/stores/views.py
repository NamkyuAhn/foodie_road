from stores.models import Category, Store, StoreImage

from django.views import View
from django.http  import JsonResponse
from django.db.models.functions import Concat
from django.db.models import CharField, Value

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
        # .annotate(
        #     storeName  = Concat('store_name', Value(''), output_field = CharField()),
        #     storeImage = Concat('image.image_urls', Value(''), output_field = CharField()),
            
        #     storeId = Concat('id', Value(''), output_field = CharField())
        #     )\
        # .values('storeName', 'storeImage', 'storeId')\
        
        return JsonResponse({'result' : results}, status = 200)