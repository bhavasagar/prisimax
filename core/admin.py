from django.contrib import admin

from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, Transaction, TravelDetails, Paytm_history, Paytm_order_history, ClubJoin, Carousal, Sizes_class, Reviews, Team, Ads, Itemimage, Itemdealer, Myorder, Sales, Categories, Extrasales, CarousalClub, ReviewsImage, Contact, FAQs


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['title', 'pincode', 'slug', 'tag', 'category']

class ClubAdmin(admin.ModelAdmin):
    search_fields = ['user__user__username']
    list_filter = ['premium', 'desig', 'fund_transfered']
    
class ItemimageAdmin(admin.ModelAdmin):
    search_fields = ['item__title']
    
class ItemdealerAdmin(admin.ModelAdmin):
    search_fields = ['item__title']
    
class MyordersAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'item__title']

class CategoriesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
class SalesAdmin(admin.ModelAdmin):
    search_fields = ['sale_name', 'item__title']

class OrdersAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'item__title']
    list_filter = ['ordered']

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_filter = ['paid_amt', 'Isclubmem']

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrdersAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Transaction)
admin.site.register(TravelDetails)
admin.site.register(ClubJoin, ClubAdmin)
admin.site.register(Paytm_order_history)
admin.site.register(Paytm_history)
admin.site.register(Carousal)
admin.site.register(CarousalClub)
admin.site.register(Sizes_class)
admin.site.register(Reviews)
admin.site.register(ReviewsImage)
admin.site.register(Team)
admin.site.register(FAQs)
admin.site.register(Contact)
admin.site.register(Itemimage, ItemimageAdmin)
admin.site.register(Itemdealer,ItemdealerAdmin)
admin.site.register(Myorder,MyordersAdmin)
admin.site.register(Sales,SalesAdmin)
admin.site.register(Extrasales,SalesAdmin)
admin.site.register(Categories,CategoriesAdmin)