from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils import timezone

CATEGORY_CHOICES = (
    ('H', 'Handicrafts'),
    ('SS', 'Sarees'),
    ('G', 'Grossery'),
    ('P','Daily Needs'),
    ('FW', 'FashionWear'),
    ('F', 'FootWear'),
    ('FU', 'Furniture'),
    ('MW', 'MensWear'),
    ('BC', 'BeautyCare'),
    ('E', 'Electronics'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

DESIGNATION = (
    ('ManagingDirector','ManagingDirector'),
    ('SubordianteDirector','SubordianteDirector'),
    ('BronzeDirector','BronzeDirector'),
    ('SilverDirector','SilverDirector'),
    ('GoldDirector','GoldDirector'),
    ('Beginner','Beginner')
)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Isclubmem = models.BooleanField(default=False)
    userphoto = models.ImageField(upload_to='images/', null=True)
    phone_number = models.CharField(default=False, max_length=20)
    def __str__(self):
        return self.user.username


class Clubmember(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE)
    refer = models.CharField(default=False,max_length=6)
    usermoney = models.FloatField(default=0.0)
    childern = models.IntegerField(default=0)
    level = models.FloatField(default=1.0)
    desig = models.CharField(default='B',choices=DESIGNATION,max_length = 20)
    travelfund = models.FloatField(default=0.0)
    teamincome = models.FloatField(default=0.0)
    downlineincome = models.FloatField(default=0.0)
    team =  models.CharField(default=False,null=True,blank=True,max_length=20)
    refered_preson = models.CharField(default=False,null=True,blank=True,max_length=20)
    def __str__(self):
        return self.user.user.username
        
class ClubJoin(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE)
    refer = models.CharField(default=False,max_length=20)
    usermoney = models.FloatField(default=0.0)
    childern = models.IntegerField(default=0)
    level = models.FloatField(default=1.0)
    desig = models.CharField(default='Beginner',choices=DESIGNATION,max_length = 20)
    referincome = models.FloatField(default=0.0)
    orderincome = models.FloatField(default=0.0)
    travelfund = models.FloatField(default=0.0)
    teamincome = models.FloatField(default=0.0)
    downlineincome = models.FloatField(default=0.0)
    team =  models.CharField(default=False,null=True,blank=True,max_length=30)
    refered_person = models.CharField(default=False,null=True,blank=True,max_length=30)
    Acno = models.CharField(default=False,null=True,blank=True,max_length=30)
    Ifsc = models.CharField(default=False,null=True,blank=True,max_length=30)
    paytm = models.CharField(default=False,null=True,blank=True,max_length=30)
    def __str__(self):
        return self.user.user.username

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    tag = models.CharField(max_length=10,blank=True,null=True,default='New')
    discount_price = models.FloatField(blank=True, null=True)
    dis_per = models.FloatField(blank=True, null=True,default=-1)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    weight = models.FloatField(default=0.5)
    pincode = models.IntegerField(default=1)
    schargeinc = models.FloatField(blank=True, null=True,default=-1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
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


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.schargeinc

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
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


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


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


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)

