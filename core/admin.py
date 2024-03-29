from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Item, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile, Transaction, TravelDetails, Paytm_history, Paytm_order_history, ClubJoin, Carousal, Sizes_class, Review, Team, Ads, Itemdealer, Myorder, Sales, Categories, Extrasales, CarousalClub, Contact, FAQs, CarousalEcommerce, Multiple_Pics, Keyword, Clickables, Notification, Pagebackground, Productbackground, Withdraw
from .forms import ItemChangeListForm
admin.site.site_header = 'Presimax administration'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Presimax'


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

def order_out_for_delivery(modeladmin, request, queryset):
    queryset.update(status='D')

def order_shipped(modeladmin, request, queryset):
    queryset.update(status='S')

def order_packed(modeladmin, request, queryset):
    queryset.update(status='P')

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
    actions = [order_out_for_delivery,order_shipped,order_packed]

class CategoriesAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
class ItemInline(admin.TabularInline):
    model = Sales.item.through    
    feilds = ['item__name']
    search_fields = ['sales__item__title']
    
class SalesAdmin(admin.ModelAdmin):
    search_fields = ['sale_name', 'item__title']
    inlines = [ItemInline]
    exclude = ('item',)

class XtraItemInline(admin.TabularInline):
    model = Extrasales.item.through    
    feilds = ['item__name']    
    
class XtraSalesAdmin(admin.ModelAdmin):
    search_fields = ['sale_name', 'item__title']
    inlines = [XtraItemInline]
    exclude = ('item',)

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
admin.site.register(Multiple_Pics)
admin.site.register(Keyword)
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
admin.site.register(CarousalEcommerce)
admin.site.register(Sizes_class)
admin.site.register(Review)
admin.site.register(Pagebackground)
admin.site.register(Ads)
admin.site.register(Productbackground)
admin.site.register(Team)
admin.site.register(FAQs)
admin.site.register(Clickables)
admin.site.register(Notification)
admin.site.register(Contact)
admin.site.register(Withdraw)
admin.site.register(Itemdealer,ItemdealerAdmin)
admin.site.register(Myorder,MyordersAdmin)
admin.site.register(Sales,SalesAdmin)
admin.site.register(Extrasales,XtraSalesAdmin)
admin.site.register(Categories,CategoriesAdmin)