from django.db.models.signals import post_save,pre_save
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils import timezone

CATEGORY_CHOICES = (
    ('H', 'Handicrafts'),
    ('SS', 'Sarees'),
    ('G', 'Grocery'),
    ('P','Daily Needs'),
    ('FW', 'Fashion Wear'),
    ('F', 'Foot Wear'),
    ('FU', 'Furniture'),
    ('MW', 'MensWear'),
    ('BC', 'Beauty Care'),
    ('E', 'Electronics'),
    ('MA', 'Mens Accessories'),
    ('WA', 'Womens Accessories'),
    ('MP','Mobiles and Mobile accessories'),
    ('HA', 'Home Appliances'),
    ('S', 'Sports'),
    ('HC', 'Health Care'),
    ('KW', 'Kids Wear'),
    ('B', 'Books'),
    ('AA', 'Auto Accessories'),
    ('J','Jewellery')
)

DELIVERY_STATUS = (
    ('R', 'Refund'),
    ('S', 'Shipped'),    
    ('P','Order Packed'),
    ('D', 'Out For Delivery'),
    ('O', 'Order Placed')
)

PAGE_OPTS = (
    ('H', 'Home'),
    ('C', 'Category'),    
    ('S','Sales')
)

NOTES = (
    ('A', 'All'),
    ('S', 'Specific')
) 

ORDER_CHOICES = (
    ('BN','Buy Now'),
    ('S', 'Save')
)

DISP_OPTS = (
    ('D','Display'),
    ('N', 'Hide')
)
    
ROW_CHOICES = (
    ('1','1'),
    ('2','2'),
)

PAYMENT_CHOICES = (
    ('P', 'Paytm'),
    ('C', 'Cash On Delivery'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
    ('I', 'indigo'),
    ('G', 'success'),
    ('B', 'blue'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

DESIGNATION = (
    ('ManagingCaption','ManagingCaption'),
    ('SubordianteCaption','SubordianteCaption'),
    ('BronzeCaption','BronzeCaption'),
    ('SilverCaption','SilverCaption'),
    ('GoldCaption','GoldCaption'),
    ('Beginner','Beginner')
)

POSITION_CHOICES = (
    ('T','TOP'),
    ('M','MIDDLE'),
    ('B','BOTTOM'),
)

SALE_NAME_CHOICES = (
    ('DOD','Deals of the day'),    
    ('FO','Flashsale On'),    
    ('DS','Sunday Sale'),
    ('DOW','Deals of this week'),    
    ('GDO','Great Discounts on')
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Isclubmem = models.BooleanField(default=False)
    userphoto = models.ImageField(upload_to='images/', null=True)
    phone_number = models.CharField(default=False, max_length=30)
    paid_amt = models.CharField(default="0", max_length=5)
    def __str__(self):
        return self.user.username      
        
class ClubJoin(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE)
    refer = models.CharField(default=False,max_length=20)
    usermoney = models.FloatField(default=0.0)
    childern = models.IntegerField(default=0)
    premium = models.BooleanField(default=False)
    level = models.FloatField(default=1.0)
    desig = models.CharField(default='Beginner',choices=DESIGNATION,max_length = 20)
    referincome = models.FloatField(default=0.0)
    prod_ref_inc = models.FloatField(default=0.0)
    orderincome = models.FloatField(default=0.0)
    travelfund = models.FloatField(default=0.0)
    teamincome = models.FloatField(default=0.0)
    downlineincome = models.FloatField(default=0.0)
    levelincome = models.FloatField(default=0.0)
    positionincome = models.FloatField(default=0.0)
    bonusincome = models.FloatField(default=0.0)
    team =  models.CharField(default=False,null=True,blank=True,max_length=30)    
    referer = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,related_name='referer',null=True,blank=True)
    Acno = models.CharField(default=False,null=True,blank=True,max_length=30)
    Ifsc = models.CharField(default=False,null=True,blank=True,max_length=30)
    paytm = models.CharField(default=False,null=True,blank=True,max_length=30)
    fund_transfered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.user.username

class Sizes_class(models.Model):
    sizes_choice = ArrayField(models.CharField(null=True, blank=True,max_length = 5), blank=True, default=list)

class Keyword(models.Model):
    word = models.CharField(max_length=100)
    
    def __str__(self):
        return self.word

class Multiple_Pics(models.Model):
    image = models.ImageField(upload_to='images/')    
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name    
 
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    pics = models.ManyToManyField(Multiple_Pics, blank=True)
    keys = models.ManyToManyField(Keyword)
    tag = models.CharField(max_length=10,blank=True,null=True,default='New')
    discount_price = models.FloatField(blank=True, null=True)
    club_discount_price = models.FloatField(blank=True, null=True,default=100000)
    dis_per = models.FloatField(blank=True, null=True,default=-1)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    pweight = models.FloatField(default=-1)
    pincode = models.IntegerField(default=123456)
    schargeinc = models.FloatField(blank=True, null=True,default=-1)
    club_schargeinc = models.FloatField(blank=True, null=True,default=-1)
    has_size = models.BooleanField(default=False,blank=True, null=True)
    size = models.ForeignKey(Sizes_class, on_delete=models.CASCADE, null=True, default=False)
    rating = models.FloatField(default=0,null=True,blank=True)
    COD = models.BooleanField(default=False,blank=True, null=True)
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self): 
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_refund_url(self):
        return reverse("core:refund", kwargs={
            'slug': self.slug
        })
    
    def get_shipping_charges_item(self):
        return float(self.schargeinc - self.discount_price)
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })



class Itemdealer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)
    additional = models.CharField(max_length=100)
    
    def __str__(self):
        return self.item.title

class Clickables(models.Model):
    url = models.URLField(max_length = 200)  
    name =  models.CharField(max_length=50) 
    
    def __str__(self):
        return self.url
        
    class Meta:
        verbose_name_plural = 'Clickables'

class Notification(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='Subscribers',blank=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=500)
    type = models.CharField(choices=NOTES,max_length=3)
    buttons = models.ManyToManyField(Clickables,related_name='Redirectors')
    
    def __str__(self):
        return self.title


class Categories(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=30)
    link = models.URLField(max_length = 200)
    slug = models.SlugField() 
    
    def __str__(self): 
        return self.name
    
    def get_absolute_url(self):
        return reverse("core:categories", kwargs={
            'slug': self.slug
        })
    
    class Meta:
        verbose_name_plural = 'Categories' 

class Sales(models.Model):
    item = models.ManyToManyField(Item)
    sale_name = models.CharField(choices=SALE_NAME_CHOICES,max_length=30)    
    caption = models.CharField(default=False,null=True,blank=True,max_length=30)    
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.sale_name
    
    def get_absolute_url(self):
        return reverse("core:sales", kwargs={
            'slug': self.sale_name
        })
    
    class Meta:
        verbose_name_plural = 'Sales'

class Extrasales(models.Model):
    item = models.ManyToManyField(Item)
    sale_name = models.CharField(max_length=30)    
    caption = models.CharField(default=False,null=True,blank=True,max_length=30)    
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.sale_name
        
    def get_absolute_url(self):
        return reverse("core:Xtrasales", kwargs={
            'slug': self.sale_name
        })
    
    class Meta:
        verbose_name_plural = 'XtraSales'



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    referer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,related_name='referer',null=True,blank=True)
    size = models.CharField(default=False,null=True,blank=True,max_length=25)
    mrp_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    price_inc_ship = models.FloatField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.price_inc_ship   

    def get_shipping_charges(self):        
        return self.price_inc_ship - self.price    

    def get_amount_saved(self):
        return self.mrp_price - self.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(choices=ORDER_CHOICES,max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.CharField(choices=PAYMENT_CHOICES,default=False,null=True,blank=True,max_length=5)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def get_total_mrp(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.mrp_price        
        return total
    
    def get_total_saved(self):
        total = 0
        for order_item in self.items.all():
            total += float(order_item.mrp_price - order_item.price)
        return total

    def get_total_ship(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.item.get_shipping_charges_item()        
        return total

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.price_inc_ship
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    phone = models.CharField(max_length=15, default=False)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Ads(models.Model):
    image = models.ImageField(upload_to='images/ads/', null=True)
    urlf = models.URLField(max_length = 200,default="https://www.presimax.online/")
    display = models.CharField(default="D",choices=DISP_OPTS,max_length=3)
    
    def __str__(self):
        return 'Ad '+str(self.id)

    class Meta:
        verbose_name_plural = 'Ads'

class Withdraw(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    granted = models.BooleanField(default=False)
    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'By {self.user.user.username} for '+str(self.amount)

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Pagebackground(models.Model):
    image = models.ImageField(upload_to='images/backgrounds/')
    font_color = models.CharField(max_length=10,default="#000")
    page = models.CharField(default="H",choices=PAGE_OPTS,max_length=3)
    
    def __str__(self):
        return str(self.id)

class Productbackground(models.Model):
    color = models.CharField(max_length=10,default="#fdde6c")
    font_color = models.CharField(max_length=10,default="#fff")
    category_font_color =  models.CharField(max_length=10,default="#fff") 
    page = models.CharField(default="H",choices=PAGE_OPTS,max_length=3)
    
    def __str__(self):
        return self.color

class TravelDetails(models.Model):
    name = models.CharField(max_length=20)
    spoint = models.CharField(max_length=20)
    epoint = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    carmodel = models.CharField(max_length=30)
    carcapacity = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'TravelDetails'


class Myorder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE,null=True,blank=True)
    myordered_date = models.DateField()
    mydelivery_date = models.DateField()
    status = models.CharField(default="O",choices=DELIVERY_STATUS,max_length=3) 
    
    def __str__(self):
        return f"{self.user.username} of {self.item.title} with {self.status}"

class Transaction(models.Model):
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)



class Paytm_order_history(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_payment_order_paytm', on_delete=models.CASCADE, null=True, default=None)
    MERC_UNQ_REF = models.IntegerField('USER ID')
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=100)
    BANKTXNID = models.CharField('BANK TXN ID', max_length=100, null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    # class Meta:
    #     app_label = 'paytm'

    def __str__(self):
        return '%s  (%s)' % (self.user.username ,self.pk)


    def __unicode__(self):
        return self.STATUS


    def __iter__(self):
        for field_name in [f.name for f in self._meta.get_fields()]:
            value = getattr(self, field_name, None)
            yield (field_name, value)
            
            
class Paytm_history(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_payment_paytm', on_delete=models.CASCADE, null=True, default=None)
    MERC_UNQ_REF = models.IntegerField('USER ID')
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=100)
    BANKTXNID = models.CharField('BANK TXN ID', max_length=100, null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    STATUS = models.CharField('STATUS', max_length=12)

    # class Meta:
    #     app_label = 'paytm'

    def __str__(self):
        return '%s  (%s)' % (self.user.username ,self.pk)


    def __unicode__(self):
        return self.STATUS


    def __iter__(self):
        for field_name in [f.name for f in self._meta.get_fields()]:
            value = getattr(self, field_name, None)
            yield (field_name, value)

class Carousal(models.Model):
    img = models.ImageField(upload_to='images/', null=True)
    head = models.CharField(max_length=15)
    des = models.CharField(max_length=100)
    urlf = models.URLField(max_length = 200)
    color = models.CharField(choices=LABEL_CHOICES, max_length=1)

class CarousalClub(models.Model):
    img = models.ImageField(upload_to='images/', null=True)
    head = models.CharField(max_length=15)
    des = models.CharField(max_length=100)
    urlf = models.URLField(max_length = 200)
    color = models.CharField(choices=LABEL_CHOICES, max_length=1)

class CarousalEcommerce(models.Model):
    img = models.ImageField(upload_to='images/', null=True)
    head = models.CharField(max_length=15)
    des = models.CharField(max_length=100)
    urlf = models.URLField(max_length = 200)
    color = models.CharField(choices=LABEL_CHOICES, max_length=1)
    position = models.CharField(choices=POSITION_CHOICES, max_length=3)
    

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_user', on_delete=models.CASCADE)
    rating = models.CharField(max_length=3,default="5")
    review = models.TextField()
    images = models.ManyToManyField(Multiple_Pics, related_name='review_images')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.item.title+" by "+self.user.username
        
    class Meta:
        verbose_name_plural = 'Reviews'

class Team(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_team', on_delete=models.CASCADE)
    name = models.CharField(max_length=20,default="HKR")
    img = models.ImageField()
    desig = models.CharField(max_length=20,default="CEO")
    opinion = models.TextField()
    team = models.CharField(default=False,null=True,blank=True,max_length=30)
    facebook = models.URLField(max_length = 200)
    twitter = models.URLField(max_length = 200)
    email = models.EmailField()
    
    def __str__(self):
        return self.user.username
        
class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name

class FAQs(models.Model):
    question = models.CharField(max_length=50)
    answer = models.CharField(max_length=500)
    
    def __str__(self):
        return self.question
        
    class Meta:
        verbose_name_plural = 'FAQs'
    
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
 
def orderitem_receiver(sender, instance, *args, **kwargs):        
    user = UserProfile.objects.get(user=instance.user)
    instance.mrp_price = float(instance.item.price)*instance.quantity    
    if user.Isclubmem:
        price = float(instance.item.club_discount_price)*instance.quantity
        instance.price = price
        instance.price_inc_ship = float(instance.item.get_shipping_charges_item())+float(price)        
    else:
        price = float(instance.item.discount_price)*instance.quantity
        instance.price = price
        instance.price_inc_ship = float(instance.item.get_shipping_charges_item())+float(price)        

def cj_receiver(sender, instance, *args, **kwargs):
    instance.usermoney = instance.travelfund + instance.teamincome + instance.downlineincome + instance.referincome + instance.orderincome + instance.bonusincome + instance.positionincome + instance.levelincome + instance.prod_ref_inc 
    if instance.level < 5:
        instance.desig = "Beginner"                        
    elif instance.level < 12 and instance.level >= 5:                        
        instance.desig = "SubordianteDirector"                        
    elif instance.level >= 12 and instance.level < 25:                        
        instance.desig = "ManagingDirector"                        
    elif instance.level >= 25 and instance.level < 50:                        
        instance.desig = "BronzeDirector"                        
    elif instance.level >= 50 and instance.level < 90:                        
        instance.desig = "SilverDirector"                        
    else:                        
        instance.desig = "GoldDirector"
    try:
        cj = ClubJoin.objects.get(id=instance.id)
        if int(float(instance.level) - float(cj.level)) >= 1:
           if int(cj.user.paid_amt) >= 500:
              instance.levelincome = instance.levelincome + 15*int(float(instance.level) - float(cj.level))
           else:
              instance.levelincome = instance.levelincome + 5*int(float(instance.level) - float(cj.level))
    except:
        pass                                     

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
pre_save.connect(orderitem_receiver, sender=OrderItem)
pre_save.connect(cj_receiver, sender=ClubJoin)