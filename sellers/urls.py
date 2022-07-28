from django.urls import path
app_name = 'sellers'
from .views import (
    AddItem,
    ItemDetailView,
    itemimgrem,
    SellerView
)
urlpatterns = [
    path('mystore/', SellerView.as_view(), name='seller-store'),
    path('additem/', AddItem.as_view(), name='AddItem'),
    path('itemdetail/<slug:slug>/', ItemDetailView.as_view(), name='itemdetail'),
    path('itemimgrem/<slug:slug>/<int:id>/',itemimgrem, name='itemimgrem'),
]
