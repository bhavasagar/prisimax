from django.urls import path
from . import views
from .views import (
    ItemDetailView,
    grossery,
    CheckoutView,
    HomeView,
    handicrafts,
    sarees,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    initiate_payment,
    callback,
    RequestRefundView,
    club
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('club/', club.as_view(), name='club'),
    path('grossery/', grossery.as_view(), name='grossery'),
    path('handicrafts/', handicrafts.as_view(), name='handicrafts'),
    path('sarees/', sarees.as_view(), name='sarees'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
    
]
