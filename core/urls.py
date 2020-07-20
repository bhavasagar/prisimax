from django.urls import path
from . import views
from django.conf.urls import (handler400, handler403, handler404, handler500)
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    AddCouponView,
    initiate_payment,
    callback,
    RequestRefundView,
    club,
    travels,
    orderpayment,
    ordercallback,
    landing,
    simp,
    privacy,
    returnpolicy,
    about,
    temp,
    sitemap,
    robots,
    Myorders,
    refund,
    Profile,
    test,
    categories,
    push,
    clubpayment,
    refreshprod,
    contact,
    faqs,
)

app_name = 'core'

urlpatterns = [
    path('ecommerce/', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('club/', club.as_view(), name='club'),
    path('travels/', travels.as_view(), name='travels'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
    path('orderpayment/', orderpayment, name='orderpayment'),
    path('ordercallback/', ordercallback, name='ordercallback'),
    path('clubpayment/', clubpayment, name='clubpayment'),
    path('', landing, name='landing'),
    path('simp/', simp, name='simp'),
    path('privacy/', privacy, name='privacy'),
    path('returnpolicy/', returnpolicy, name='returnpolicy'),
    path('about/', about, name='about'),
    path('tests/', temp.as_view(), name='temp'),
    path('sitemap.xml/', sitemap, name='sitemap.xml'),
    path('robots.txt/', robots, name='robots.txt'),
    path('myorders/', Myorders.as_view(), name='myorders'),
    path('refund/<slug>/', refund, name='refund'),
    path('profile/', Profile.as_view(), name='Profile'),
    path('refreshpaid/', test, name='test'),
    path('refreshprod/', refreshprod, name='refreshprod'),
    path('sw.js/', push, name='push'),
    path('categories/<slug>/', categories, name='categories'),
    path('contact/', contact, name='contact'),
    path('faqs/', faqs, name='faqs'),
]