from django.urls import path
from stores.views import StoreListView, StoreDetailView

urlpatterns = [
    path('/list/<int:ct_id>', StoreListView.as_view()),
    path('/<int:store_id>', StoreDetailView.as_view()),
]