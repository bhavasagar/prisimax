from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.utils import timezone
from django.utils.text import slugify
from core.models import Item,Sizes_class,Multiple_Pics,Keyword

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

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
    ('I', 'indigo'),
    ('G', 'success'),
    ('B', 'blue'),
)


class SellerItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=2)
    title = models.CharField(max_length=100)
    price = models.FloatField()    
    tag = models.CharField(max_length=10,blank=True,null=True,default='New')
    discount_price = models.FloatField(blank=True, null=True)
    club_discount_price = models.FloatField(blank=True, null=True,default=100000)
    dis_per = models.FloatField(blank=True, null=True,default=-1)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1,default="P")
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField()
    pis = models.ManyToManyField(Multiple_Pics, blank=True)
    kys = models.ManyToManyField(Keyword, blank=True)
    pweight = models.FloatField(default=-1)
    pincode = models.IntegerField(default=123456)    
    has_size = models.BooleanField(default=False,blank=True, null=True)
    size = models.CharField(null=True, default=False,max_length=100)
    rating = models.FloatField(default=0,null=True,blank=True)
    COD = models.BooleanField(default=False,blank=True, null=True)
    review = models.BooleanField(default=False)
    item_created = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Item.objects.filter(slug=unique_slug).exists() or SellerItem.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
        
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

def item_receiver(sender, instance, *args, **kwargs):
    if instance.review:        
        try:
            item = Item.objects.filter(slug=instance.slug)
            item.delete()
        except:
            pass
        item = Item.objects.create(
        title=instance.title,
        tag=instance.tag,
        image=instance.image,
        price=instance.price,
        description=instance.description)   
        instance.item_created=item 
        item.size=None                
        if instance.has_size:
            item.has_size=True 
            szs = str(instance.size).split(',')
            s, created = Sizes_class.objects.get_or_create(sizes_choice=szs)               
            item.size=s
        for i in item.pics.all():
            item.pics.remove(i)
        for i in instance.pis.all():
            item.pics.add(i)        
        item.slug=instance.slug
        item.pweight=instance.pweight
        item.category=instance.category        
        instance.review=False
        item.save()
        instance.save()

pre_save.connect(item_receiver, sender=SellerItem)