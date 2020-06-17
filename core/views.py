from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, Transaction, TravelDetails, ClubJoin, Paytm_order_history,Paytm_history
import random
import string
import stripe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .paytm import generate_checksum, verify_checksum
from django.core.paginator import Paginator


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, *args, **kwargs):
        if self.request.user.userprofile.Isclubmem:
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                form = CheckoutForm()
                context = {
                    'form': form,
                    'couponform': CouponForm(),
                    'order': order,
                    'DISPLAY_COUPON_FORM': True
                }
    
                shipping_address_qs = Address.objects.filter(
                    user=self.request.user,
                    address_type='S',
                    default=True
                )
                if shipping_address_qs.exists():
                    context.update(
                        {'default_shipping_address': shipping_address_qs[0]})
    
                billing_address_qs = Address.objects.filter(
                    user=self.request.user,
                    address_type='B',
                    default=True
                )
                if billing_address_qs.exists():
                    context.update(
                        {'default_billing_address': billing_address_qs[0]})
    
                return render(self.request, "checkout.html", context)
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")
        else:
            return redirect("core:club")

    def post(self, *args, **kwargs):
        if self.request.user.userprofile.Isclubmem:
            form = CheckoutForm(self.request.POST or None)
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                if form.is_valid():
    
                    use_default_shipping = form.cleaned_data.get(
                        'use_default_shipping')
                    if use_default_shipping:
                        print("Using the defualt shipping address")
                        address_qs = Address.objects.filter(
                            user=self.request.user,
                            address_type='S',
                            default=True
                        )
                        if address_qs.exists():
                            shipping_address = address_qs[0]
                            order.shipping_address = shipping_address
                            order.save()
                        else:
                            messages.info(
                                self.request, "No default shipping address available")
                            return redirect('core:checkout')
                    else:
                        print("User is entering a new shipping address")
                        shipping_address1 = form.cleaned_data.get(
                            'shipping_address')
                        shipping_address2 = form.cleaned_data.get(
                            'shipping_address2')
                        shipping_country = form.cleaned_data.get(
                            'shipping_country')
                        shipping_zip = form.cleaned_data.get('shipping_zip')
    
                        if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                            shipping_address = Address(
                                user=self.request.user,
                                street_address=shipping_address1,
                                apartment_address=shipping_address2,
                                country=shipping_country,
                                zip=shipping_zip,
                                address_type='S'
                            )
                            shipping_address.save()
    
                            order.shipping_address = shipping_address
                            order.save()
    
                            set_default_shipping = form.cleaned_data.get(
                                'set_default_shipping')
                            if set_default_shipping:
                                shipping_address.default = True
                                shipping_address.save()
    
                        else:
                            messages.info(
                                self.request, "Please fill in the required shipping address fields")
    
                    use_default_billing = form.cleaned_data.get(
                        'use_default_billing')
                    same_billing_address = form.cleaned_data.get(
                        'same_billing_address')
    
                    if same_billing_address:
                        billing_address = shipping_address
                        billing_address.pk = None
                        billing_address.save()
                        billing_address.address_type = 'B'
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
    
                    elif use_default_billing:
                        print("Using the defualt billing address")
                        address_qs = Address.objects.filter(
                            user=self.request.user,
                            address_type='B',
                            default=True
                        )
                        if address_qs.exists():
                            billing_address = address_qs[0]
                            order.billing_address = billing_address
                            order.save()
                        else:
                            messages.info(
                                self.request, "No default billing address available")
                            return redirect('core:checkout')
                    else:
                        print("User is entering a new billing address")
                        billing_address1 = form.cleaned_data.get(
                            'billing_address')
                        billing_address2 = form.cleaned_data.get(
                            'billing_address2')
                        billing_country = form.cleaned_data.get(
                            'billing_country')
                        billing_zip = form.cleaned_data.get('billing_zip')
    
                        if is_valid_form([billing_address1, billing_country, billing_zip]):
                            billing_address = Address(
                                user=self.request.user,
                                street_address=billing_address1,
                                apartment_address=billing_address2,
                                country=billing_country,
                                zip=billing_zip,
                                address_type='B'
                            )
                            billing_address.save()
    
                            order.billing_address = billing_address
                            order.save()
    
                            set_default_billing = form.cleaned_data.get(
                                'set_default_billing')
                            if set_default_billing:
                                billing_address.default = True
                                billing_address.save()
    
                        else:
                            messages.info(
                                self.request, "Please fill in the required billing address fields")
    
                    payment_option = form.cleaned_data.get('payment_option')
    
                    if payment_option == 'P':
                        return redirect('core:orderpayment')
                    else:
                        messages.warning(
                            self.request, "Invalid payment option selected")
                        return redirect('core:checkout')
            except ObjectDoesNotExist:
                messages.warning(self.request, "You do not have an active order")
                return redirect("core:order-summary")
                
        else:
            return redirect("core:club")


@login_required
def orderpayment(request):
    order = Order.objects.get(user=request.user, ordered=False)
    amount = int(order.get_total())
    transaction = Transaction.objects.create(made_by=request.user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'https://www.presimax.online/ordercallback/'),
        ('MERC_UNQ_REF', str(request.user.id)),     
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == "POST":
        user = request.user
        MERCHANT_KEY = settings.PAYTM_SECRET_KEY
        data_dict = {}
        data_dict = dict(request.POST.items())

        verify = verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])             #verifing checksum
        if verify:
            for key in request.POST:                                                                      #converting string to float
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            Paytm_history.objects.create(user_id = data_dict['MERC_UNQ_REF'], **data_dict)                 #saving data
            return render(request, "callback.html", {"paytm":data_dict, 'user': user})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)


@login_required
def initiate_payment(request):
    transaction = Transaction.objects.create(made_by=request.user, amount=500)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'https://www.presimax.online/callback/'),
        ('MERC_UNQ_REF', str(request.user.id)),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def ordercallback(request):
    if request.method == "POST":
        user = request.user
        MERCHANT_KEY = settings.PAYTM_SECRET_KEY
        data_dict = {}
        data_dict = dict(request.POST.items())

        verify = verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])             #verifing checksum
        if verify:
            for key in request.POST:                                                                      #converting string to float
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            Paytm_order_history.objects.create(user_id = data_dict['MERC_UNQ_REF'], **data_dict)
            if data_dict['STATUS'] == 'TXN_SUCCESS':
                cust = User.objects.get(id=data_dict['MERC_UNQ_REF'])
                order = Order.objects.get(user=cust, ordered=False)
                qs = order.items.all()
                amt = 0
                for oi in qs:
                    amt+= float(oi.get_amount_saved())
                order.ordered = True
                order.save()
                up = UserProfile.objects.get(user=cust)
                cm = ClubJoin.objects.get(user=up)
                cm.orderincome = cm.orderincome+(amt)*0.1
                cm.save()
            return render(request, "ordercallback.html", {"paytm":data_dict, 'user': user})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

def landing(request):
    return render(request, 'index.html')

class HomeView(ListView):
    qs = Item.objects.filter(dis_per=-1)
    for i in qs:
        i.dis_per = ((i.price - i.discount_price)/i.price)*100
        i.save()
    sqs = Item.objects.filter(schargeinc=-1)
    for i in qs:
        if i.discount_price:
            if i.weight <= 0.5:
                i.schargeinc=i.discount_price+58
            elif i.weight <= 1:
                i.schargeinc=i.discount_price+85
            elif i.weight <= 2:
                i.schargeinc=i.discount_price+120
            elif i.weight <=5:
                i.schargeinc=i.discount_price+235
            else:
                i.schargeinc=i.discount_price+240
            i.save()
        else:
            if i.weight <= 0.5:
                i.schargeinc=i.price+58
            elif i.weight <= 1:
                i.schargeinc=i.price+85
            elif i.weight <= 2:
                i.schargeinc=i.price+120
            elif i.weight <=5:
                i.schargeinc=i.price+235
            else:
                i.schargeinc=i.price+240
            i.save()
    model = Item
    paginate_by = 10
    template_name = "home.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)
            

class travels(ListView):
    model = TravelDetails
    template_name = "travels.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            travel_details = TravelDetails.objects.create(
                name = self.request.POST.get('name'),
                spoint = self.request.POST.get('spoint'),
                epoint = self.request.POST.get('epoint'),
                phonenumber = self.request.POST.get('phonenumber')
            )
            travel_details.email = self.request.POST.get('email')
            travel_details.carmodel = self.request.POST.get('carmodel')
            travel_details.carcapacity = self.request.POST.get('carcapacity')
            travel_details.save()
            messages.info(self.request,'We will contact you soon about travel details. Thank you')
            return redirect('core:home')
        return render(self.request,self.template_name)


class club(View):
    template_name = "club.html"
    def get(self,*args,**kwargs):
        if self.request.user.userprofile.Isclubmem:
            club_member = ClubJoin.objects.filter(user=self.request.user.userprofile)
            downliners = ClubJoin.objects.filter(refered_person=self.request.user.username)
            for cm in club_member:
                cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome
                cm.save()
            for cm in downliners:
                cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome
                cm.save()
            if club_member[0].team!="False":
                team = ClubJoin.objects.filter(team=club_member[0].team)
                for cm in team:
                    cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome
                    cm.save()
            context = {
                'club_member': club_member,
                'downliners':downliners,
            }
            if club_member[0].team!="False":
                  context['team']=team
            return render(self.request,self.template_name,context=context)
        elif len(Paytm_history.objects.filter(user=self.request.user, STATUS='TXN_SUCCESS'))<1:
            return redirect('/pay')
        return render(self.request,self.template_name)
    def post(self, *args ,**kwargs):
        if not self.request.user.userprofile.Isclubmem:
            if self.request.method == 'POST':
                self.request.user.userprofile.userphoto = self.request.FILES.get('image')
                self.request.user.userprofile.phone_number = self.request.POST.get('userphonenumber')
                self.request.user.userprofile.Isclubmem = True
                k = refgenrator('any')
                while len(ClubJoin.objects.filter(refer = k))>1:
                    k = refgenrator('any')
                club_member = ClubJoin.objects.create(
                    user = self.request.user.userprofile,
                    refer = k,
                )
                if (len(self.request.POST.get('acno'))>0 and len(self.request.POST.get('ifsc'))>0) or len(self.request.POST.get('paytm'))>0: 
                    if (len(self.request.POST.get('acno'))>0 and len(self.request.POST.get('ifsc'))>0):
                        club_member.Acno = self.request.POST.get('acno')
                        club_member.Ifsc = self.request.POST.get('ifsc')
                    else:
                        club_member.paytm = self.request.POST.get('paytm')
                else:
                    return redirect('core:club')
                ref = self.request.POST.get('referalcode')
                if len(ref)>0:
                    try:
                        referer = ClubJoin.objects.filter(refer=ref).first()
                        referer.childern += 1
                        referer.level = int(referer.childern/3)+1
                        club_member.refered_person = referer.user.user.username 
                        referer.save()
                    except:
                        pass
                club_member.save()
                self.request.user.userprofile.save()
                return redirect('core:home')
        elif len(Paytm_history.objects.filter(user=self.request.user, STATUS='TXN_SUCCESS'))>0:
            return redirect('/pay')
import random as rd
def refgenrator(name):
    l=rd.choices(range(41,94),k=6)
    c=""
    for i in range(len(l)):
        c+=chr(l[i])
    return str(c)
    
class grossery(ListView):
    model = Item
    paginate_by = 10
    template_name = "grossery.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class sarees(ListView):
    model = Item
    paginate_by = 10
    template_name = "sarees.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class handicrafts(ListView):
    model = Item
    paginate_by = 10
    template_name = "handicrafts.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)
    
class dailyneeds(ListView):
    model = Item
    paginate_by = 10
    template_name = "dailyneeds.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class fashionwear(ListView):
    model = Item
    paginate_by = 10
    template_name = "fashionwear.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class footwear(ListView):
    model = Item
    paginate_by = 10
    template_name = "footwear.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)
    
class menswear(ListView):
    model = Item
    paginate_by = 10
    template_name = "menwear.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class beautycare(ListView):
    model = Item
    paginate_by = 10
    template_name = "beautycare.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class furniture(ListView):
    model = Item
    paginate_by = 10
    template_name = "furniture.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class electronics(ListView):
    model = Item
    paginate_by = 10
    template_name = "electronics.html"
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            query = self.request.POST.get('search')
            qs = Item.objects.filter(title__icontains=query)
            context = { 'sobs': qs}
            if len(qs)<1:
                messages.info(self.request, "Invalid search")
                return redirect('/')
            return render(self.request, 'search.html', context=context)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")