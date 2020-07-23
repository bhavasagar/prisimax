from django.db.models.signals import post_save
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
    
ROW_CHOICES = (
    ('1','1'),
    ('2','2'),
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
    ('DOD','Deals of the Day'),
    ('NA','New Arrivals'),
    ('FO','FlashSale On'),
    ('BSP','BestSeller Products'),
    ('DS','Sunday Sale'),
    ('DOW','Deals of this Week'),
    ('MTTDP','More than 30% Off on discount price'),
    ('GDO','Great Discounts on'),
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
    orderincome = models.FloatField(default=0.0)
    travelfund = models.FloatField(default=0.0)
    teamincome = models.FloatField(default=0.0)
    downlineincome = models.FloatField(default=0.0)
    levelincome = models.FloatField(default=0.0)
    positionincome = models.FloatField(default=0.0)
    bonusincome = models.FloatField(default=0.0)
    team =  models.CharField(default=False,null=True,blank=True,max_length=30)
    refered_person = models.CharField(default=False,null=True,blank=True,max_length=30)
    Acno = models.CharField(default=False,null=True,blank=True,max_length=30)
    Ifsc = models.CharField(default=False,null=True,blank=True,max_length=30)
    paytm = models.CharField(default=False,null=True,blank=True,max_length=30)
    fund_transfered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.user.username

class Sizes_class(models.Model):
    sizes_choice = ArrayField(models.CharField(null=True, blank=True,max_length = 5), blank=True, default=list)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
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
    selcsize = models.CharField(default=False,null=True,blank=True,max_length=25)
    
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
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

class Itemsearch(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    searchwords = models.CharField(max_length=100)
    
    def __str__(self):
        return self.item.title

class Itemdealer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30)
    additional = models.CharField(max_length=100)
    
    def __str__(self):
        return self.item.title

class Itemimage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    img = models.ImageField()
    
    def __str__(self):
        return self.item.title

class Myorder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    myordered_date = models.DateField()
    mydelivery_date = models.DateField()
    status = models.CharField(default="404",null=True,blank=True,max_length=25) 
    
    def __str__(self):
        return f"{self.user.username} of {self.item.title} with {self.status}"

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
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sale_name = models.CharField(choices=SALE_NAME_CHOICES,max_length=30)
    day = models.CharField(default=False,null=True,blank=True,max_length=30)
    caption = models.CharField(default=False,null=True,blank=True,max_length=30)
    row = models.CharField(choices=ROW_CHOICES,default=False,null=True,blank=True,max_length=30)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.sale_name
    
    class Meta:
        verbose_name_plural = 'Sales'

class Extrasales(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    sale_name = models.CharField(max_length=30)
    day = models.CharField(default=False,null=True,blank=True,max_length=30)
    caption = models.CharField(default=False,null=True,blank=True,max_length=30)
    row = models.CharField(choices=ROW_CHOICES,default=False,null=True,blank=True,max_length=30)
    
    def __str__(self):
        return self.sale_name
    
    class Meta:
        verbose_name_plural = 'XtraSales'


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(default=False,null=True,blank=True,max_length=25)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_club_shipping_charges(self):
        if self.item.club_discount_price:
            return self.item.club_schargeinc - self.item.club_discount_price
        return self.item.club_schargeinc - self.item.discount_price
    
    def get_shipping_charges(self):
        if self.item.discount_price:
            return self.item.schargeinc - self.item.discount_price
        return self.item.schargeinc - self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.schargeinc
    
    def get_total_club_discount_item_price(self):
        return self.quantity * self.item.club_schargeinc

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_club_amount_saved(self):
        return self.get_total_item_price() - self.get_total_club_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
    def get_club_final_price(self):
        if self.item.discount_price:
            return self.get_total_club_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    def get_club_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_club_final_price()
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
    image = models.ImageField(upload_to='images/adds/', null=True)
    text = models.CharField(max_length=20)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES)
    typeoa = models.CharField(max_length=20)
    
    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Ads'

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


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

class Reviews(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_user', on_delete=models.CASCADE)
    rating = models.CharField(max_length=3,default="5")
    review = models.TextField()
    
    def __str__(self):
        return self.item.title+" by "+self.user.username
        
    class Meta:
        verbose_name_plural = 'Reviews'

class ReviewsImage(models.Model):
    post = models.ForeignKey(Reviews, related_name='Reviewsimages', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='reviewimages')

    def __str__(self):
        return '%s - %s ' % (self.post.item.title, self.post.user.username)

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
 

post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)