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
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, Transaction, TravelDetails, ClubJoin, Paytm_order_history,Paytm_history, Carousal, Reviews, Team, Ads, Itemdealer, Myorder, Categories, Sales, CarousalClub, ReviewsImage, Contact, FAQs
import random
from django.shortcuts import reverse
import string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .paytm import generate_checksum, verify_checksum
import smtplib
from django.core.paginator import Paginator
from email.message import EmailMessage
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models.functions import ( ExtractDay, ExtractHour, ExtractMinute, ExtractMonth, ExtractSecond, ExtractWeek, ExtractWeekDay, ExtractYear )

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

    def post(self, *args, **kwargs):
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
                        shipping_address.phone = form.cleaned_data.get('shipping_phone')
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
                        return redirect("core:order-summary")
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
                        billing_address.phone = form.cleaned_data.get('billing_phone')
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
                        return redirect("core:order-summary")

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

@login_required
def clubpayment(request):
    if request.user.userprofile.paid_amt == "500":
        return redirect("core:club")
    else:
        if request.method == "GET":
            return render(request, 'clubselect.html')
        try:
            amt = int(request.POST['amt'])
        except:
            return render(request, 'clubselect.html', context={'error': 'Wrong Details or amount'})
        transaction = Transaction.objects.create(made_by=request.user, amount=amt)
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
    

@login_required
def orderpayment(request):
    order = Order.objects.get(user=request.user, ordered=False)
    if request.user.userprofile.Isclubmem:
        amount = int(order.get_club_total())
    else:
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
            Paytm_history.objects.create(user_id = data_dict['MERC_UNQ_REF'], **data_dict)
            cust = User.objects.get(id=data_dict['MERC_UNQ_REF'])
            server = smtplib.SMTP_SSL('smtp.gmail.com',465)
            server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi') 
            if data_dict['STATUS'] == 'TXN_SUCCESS':
                up = UserProfile.objects.get(user=cust)
                up.paid_amt = str(int(up.paid_amt)+int(data_dict["TXNAMOUNT"]))
                up.save()
                if int(up.paid_amt) >= 500:
                    cm = ClubJoin.objects.get(user=up)
                    cm.premium = True
                    cm.save()
                msg = EmailMessage()
                msg.set_content("This is a computer generated email don't reply to this mail.\n This mail is to confirm your entry to our club with entry fee Rs." + str(data_dict["TXNAMOUNT"]) + " . Thank you for joining to our club.\nPlease click on club in navagation bar again to fill your details and enjoy our services as a club member.")
                msg['Subject'] = 'Presimax-online shopping and money earning'
                msg['From'] = "presimaxinfo@gmail.com"
                msg['To'] = cust.email
                server.send_message(msg)
                msg1 = EmailMessage()
                msg1.set_content("This is a computer generated email don't reply to this mail.\n This mail is to confirm "+ str(cust.email) +" entry to our club with entry fee Rs." + str(data_dict["TXNAMOUNT"]) + " . Thank you for joining to our club.\nPlease click on club in navagation bar again to fill your details and enjoy our services as a club member.")
                msg1['Subject'] = 'New member Joined'
                msg1['From'] = "presimaxinfo@gmail.com"
                msg1['To'] = "powerstarcharan666@gmail.com"
                server.send_message(msg1)
                server.quit()
                msg = "PS"
            else:
                msg = EmailMessage()
                msg.set_content("This is a computer generated email don't reply to this mail.\n This mail is to report your entry attempt to our club has failed. Join to our club to enjoy our services.")
                msg['Subject'] = 'Presimax-online shopping and money earning'
                msg['From'] = "presimaxinfo@gmail.com"
                msg['To'] = cust.email
                server.send_message(msg)
                server.quit()
                msg="PF"
            oid =  str(data_dict['ORDERID'])
            ta =  str(data_dict['TXNAMOUNT'])
            return render(request, "callback.html", {"paytm":data_dict, 'user': user, 'msg':msg, 'oid':oid, 'ta':ta})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)


@login_required
def initiate_payment(request):
    transaction = Transaction.objects.create(made_by=request.user, amount=250)
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
            msg = "PF"
            oid =  str(data_dict['ORDERID'])
            ta =  str(data_dict['TXNAMOUNT'])
            if data_dict['STATUS'] == 'TXN_SUCCESS':
                cust = User.objects.get(id=data_dict['MERC_UNQ_REF'])
                server = smtplib.SMTP_SSL('smtp.gmail.com',465)
                server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi') 
                if data_dict['STATUS'] == 'TXN_SUCCESS':
                    msg = EmailMessage()
                    recipients = ['hemanthraju9966@gmail.com', 'navi87362@gmail.com']
                    msg.set_content("This is a computer generated email don't reply to this mail.\n This mail is to confirm your order on PRESIMAX of Rs." + str(data_dict["TXNAMOUNT"]) + " with order Id "+ str(data_dict["ORDERID"]) + " by "+ str(cust.username) +".\nThank you for purchasing. Visit us again.")
                    msg['Subject'] = 'Order Confirmation'
                    msg['From'] = "presimaxinfo@gmail.com"
                    msg['To'] = ", ".join(recipients)
                    server.send_message(msg)
                    msg1 = EmailMessage()
                    msg1.set_content("This is a computer generated email don't reply to this mail.\n This mail is to confirm your order on PRESIMAX of Rs." + str(data_dict["TXNAMOUNT"]) + " with order Id "+ str(data_dict["ORDERID"]) +".\nThank you for purchasing. Visit us again.")
                    msg1['Subject'] = 'Order Confirmation'
                    msg1['From'] = "presimaxinfo@gmail.com"
                    msg1['To'] = cust.email
                    server.send_message(msg1)
                    server.quit()
                order = Order.objects.get(user=cust, ordered=False)
                qs = order.items.all()
                amt = data_dict["TXNAMOUNT"]
                oitms = OrderItem.objects.filter(user=cust, ordered=False)
                for i in oitms:
                    i.ordered = True
                    myorder = Myorder.objects.create(user=cust,item=i.item,myordered_date=datetime.now(),mydelivery_date=datetime.now()+timedelta(days=5))
                    i.save()
                order.ordered = True
                order.save()
                up = UserProfile.objects.get(user=cust)
                cm = ClubJoin.objects.get(user=up)
                cm.level = cm.level + round((amt/3000),1)
                if int(cm.user.paid_amt) >= 500: 
                    cm.orderincome = cm.orderincome+(amt)*0.1
                else:
                    cm.orderincome = cm.orderincome+(amt)*0.05
                if cm.level == int(cm.level):
                    if int(cm.user.paid_amt) >= 500:
                        cm.levelincome = cm.levelincome + 15
                    else:
                        cm.levelincome = cm.levelincome + 5 
                try:
                    refuser = User.objects.get(username=cm.refered_person)
                    rup = UserProfile.objects.get(user=refuser)
                    ref = ClubJoin.objects.get(user=rup)
                    if int(referer.user.paid_amt) >= 500:                    
                        ref.downlineincome = ref.downlineincome + (amt)*0.01
                    else:
                        ref.downlineincome = ref.downlineincome + (amt)*0.007
                    ref.save()
                except:
                    pass
                msg = "PS"
            return render(request, "ordercallback.html", {"paytm":data_dict, 'user': user, 'msg':msg, 'oid':oid, 'ta':ta})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

def landing(request):
    carousal = Carousal.objects.all()[0]
    carousal1 = Carousal.objects.all()[1]
    carousal2 = Carousal.objects.all()[2]
    carousal3 = Carousal.objects.all()[3]
    carousal4 = Carousal.objects.all()[4]
    return render(request, 'index.html', {'item':carousal,'item1':carousal1,'item2':carousal2,'item3':carousal3,'item4':carousal4})
    
def simp(request):
    item = Item.objects.all()
    context={'items':item}
    return render(request, 'similarprod.html', context=context)

class HomeView(ListView):
    template_name = "home.html"
    def get(self,*args, **kwargs):
        items = Item.objects.all().order_by('-id')[0:7]
        items1 = Item.objects.all().order_by('-id')[9:16]
        items2 = Item.objects.filter(dis_per__gte=30)[0:7]
        items3 = Item.objects.filter(dis_per__gte=30).order_by('-id')[9:16]
        items4 = Item.objects.filter(dis_per__gte=70).order_by('-id')
        items7 = Item.objects.filter(tag="BESTSELLER").order_by('-id')[0:7]
        items6 = Item.objects.filter(tag="BESTSELLER")[9:16]
        items8 = Sales.objects.filter(sale_name="DOW")
        items11 = Sales.objects.filter(sale_name="DS")[0:7]
        items12 = Sales.objects.filter(sale_name="DS")[9:16]
        items9 = Sales.objects.filter(sale_name="DOD")
        items10 = Sales.objects.filter(sale_name="FO")
        categories = Categories.objects.all()
        context={'object_list':items,'object_list1':items1,'cat':categories,'object_list2':items2,'object_list3':items3,'object_list4':items4,'object_list6':items6,'object_list7':items7,'object_list8':items8,'object_list9':items9,'object_list10':items10,'object_list11':items11,'object_list12':items12}
        if datetime.now().strftime("%A")!="Sunday":
            context["status"]="disabled"
            context["msg"]="Wait up to SUNDAY for this sale..."
        now = timezone.now()
        if len(items10)>0:
            sdate = items10[0].start
            edate = items10[0].end
            today = datetime.today()
            if sdate < now:
                context["day"]=edate.day - now.day
                context["hours"]=edate.hour
                context["minutes"]=edate.minute
                context["seconds"]=edate.second
                context["fmsg"]="Ends In"
            else:
                context["day"]=-sdate.day + now.day
                context["hours"]=sdate.hour
                context["minutes"]=sdate.minute
                context["seconds"]=sdate.second
                context["fmsg"]="Starts In"
            if sdate > now:
                context["fstatus"]="disabled"
        return render(self.request, self.template_name, context)
    def post(self,*args,**kwargs):
        if self.request.method == 'POST':
            if self.request.POST.get('search'):
                query = self.request.POST.get('search')
                qs = Item.objects.filter(Q(title__search=query)|Q(category__search=query)|Q(description__search=query))
                msg = 'Search results'
                context = { 'sobs': qs , 'type':msg}
                if len(qs)<1:
                    messages.info(self.request, "Invalid search")
                    return redirect('/ecommerce/')
            else:
                min_price = int(self.request.POST.get('min_price'))-int(self.request.POST.get('min_price'))*0.1
                max_price = int(self.request.POST.get('max_price'))+int(self.request.POST.get('max_price'))*0.1
                min_dis_per = int(self.request.POST.get('min_dis_price'))-int(self.request.POST.get('min_dis_price'))*0.1
                max_dis_per = int(self.request.POST.get('max_dis_price'))+int(self.request.POST.get('max_dis_price'))*0.1
                if self.request.POST.get('new'):
                    qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(tag="New")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
                if self.request.POST.get('bestseller'):
                    qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(tag="BESTSELLER")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
                if self.request.POST.get('bestseller') and self.request.POST.get('new'):
                    qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(tag="New")&Q(tag="BESTSELLER")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
                if not (self.request.POST.get('bestseller') and self.request.POST.get('new')):
                    qs = Item.objects.filter(Q(dis_per__gte=min_dis_per)&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
                if len(qs)>36:
                    qs = qs[0:36]
                msg = 'Filter results'
                context = { 'sobs': qs , 'type':msg}
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
        if self.request.user.is_authenticated:
            if self.request.user.userprofile.Isclubmem:
                club_member = ClubJoin.objects.filter(user=self.request.user.userprofile)
                downliners = ClubJoin.objects.filter(refered_person=self.request.user.username)
                mn,mx=0,5
                for cm in club_member:
                    cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome + cm.bonusincome + cm.positionincome + cm.levelincome
                    if cm.level<5:
                        cm.desig = "Beginner"
                        clr = 'purple'
                    elif cm.level<12 and cm.level>=5:
                        mn,mx=5,12
                        cm.desig = "SubordianteDirector"
                        clr = 'pink'
                    elif cm.level>=12 and cm.level<25:
                        mn,mx=12,25
                        cm.desig = "ManagingDirector"
                        clr = 'yellow'
                    elif cm.level>=25 and cm.level<50:
                        mn,mx=25,50
                        cm.desig = "BronzeDirector"
                        clr = 'green'
                    elif cm.level>=50 and cm.level<90:
                        mn,mx=50,90
                        cm.desig = "SilverDirector"
                        clr = 'red'
                    else:
                        mn,mx=90,150
                        cm.desig = "GoldDirector"
                        clr = 'blue'
                    cm.save()
                    
                    nw = (cm.level-int(cm.level))*100
                for cm in downliners:
                    cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome + cm.bonusincome + cm.positionincome + cm.levelincome + cm.bonusincome + cm.positionincome + cm.levelincome
                    cm.save()
                if club_member[0].team!="False":
                    team = ClubJoin.objects.filter(team=club_member[0].team)
                    for cm in team:
                        cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome + cm.bonusincome + cm.positionincome + cm.levelincome + cm.bonusincome + cm.positionincome + cm.levelincome
                        cm.save()
                carousal = CarousalClub.objects.get(pk=1)
                carousal1 = CarousalClub.objects.all().exclude(pk=1)
                context = {
                    'club_member': club_member,
                    'downliners':downliners,
                    'citems':carousal1,
                    'item':carousal
                }
                context['min']=mn
                context['max']=mx
                context['now']=nw
                context['color']=clr
                if club_member[0].team!="False":
                      context['team']=team                
                return render(self.request,self.template_name,context=context)
            elif len(Paytm_history.objects.filter(user=self.request.user, STATUS='TXN_SUCCESS'))<1:
                return redirect('/clubpayment/')
            else:
                gtype = "hidden"
                if len(self.request.user.email)<11:
                    self.request.user.email = self.request.POST.get('email')
                    gtype = "text"
                return render(self.request,self.template_name,{'type':gtype})
        else:
            return redirect('/accounts/login')
    def post(self, *args ,**kwargs):
        if self.request.user.is_authenticated:
            if not self.request.user.userprofile.Isclubmem:
                if self.request.method == 'POST':
                    if len(self.request.user.email)<11:
                        self.request.user.email = self.request.POST.get('email')
                        
                    self.request.user.userprofile.userphoto = self.request.FILES.get('image')
                    if (len(self.request.POST.get('userphonenumber'))>9 and len(self.request.POST.get('userphonenumber'))<20): 
                        self.request.user.userprofile.phone_number = self.request.POST.get('userphonenumber')
                    else:
                        messages.info(self.request, "Enter a valid Phone number")
                        return redirect('core:club')
                    self.request.user.userprofile.Isclubmem = True
                    k = refgenrator('any')
                    while len(ClubJoin.objects.filter(refer = k))>1:
                        k = refgenrator('any')
                    if not self.request.POST.get('checkbox'):
                        messages.warning(self.request, "Check the box down...")
                        return redirect('core:club')
                    if (len(self.request.POST.get('acno'))>0 and len(self.request.POST.get('ifsc'))>0) or len(self.request.POST.get('paytm'))>0: 
                        if (len(self.request.POST.get('acno'))>0 and len(self.request.POST.get('ifsc'))>0):
                            club_member = ClubJoin.objects.create(
                                user = self.request.user.userprofile,
                                refer = k,
                            )
                            club_member.Acno = self.request.POST.get('acno')
                            club_member.Ifsc = self.request.POST.get('ifsc')
                        else:
                            club_member = ClubJoin.objects.create(
                                user = self.request.user.userprofile,
                                refer = k,
                            )
                            club_member.paytm = self.request.POST.get('paytm')
                    else:
                        messages.info(self.request, "Enter valid Account number and IFSC code or Paytm number")
                        return redirect('core:club')
                    ref = self.request.POST.get('referalcode')
                    if len(ref)>0:
                        try:
                            referer = ClubJoin.objects.filter(refer=ref).first()
                            referer.childern += 1
                            referer.level = referer.level+0.2
                            if referer.level == int(referer.level):
                                if int(referer.user.paid_amt) >= 500:
                                    referer.levelincome = referer.levelincome + 15
                                else:
                                    referer.levelincome = referer.levelincome + 5 
                            if (int(referer.user.paid_amt) >= 500) and int(self.request.user.userprofile.paid_amt)>=500:
                                referer.referincome = referer.referincome + 100
                            else:
                                referer.referincome = referer.referincome + 50
                            club_member.refered_person = referer.user.user.username 
                            referer.save()
                        except:
                            pass
                    club_member.save()
                    self.request.user.userprofile.save()
                    return redirect("core:home")
            elif len(Paytm_history.objects.filter(user=self.request.user, STATUS='TXN_SUCCESS'))>0:
                return redirect('/clubpayment/')
        else:
            return redirect('/accounts/login')
            
import random as rd
def refgenrator(name):
    l=rd.choices(range(65,90),k=6)
    c=""
    for i in range(len(l)):
        c+=chr(l[i])
    return str(c)

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
            return redirect("/ecommerce/")
            

class ItemDetailView(DetailView):
    template_name = "product.html"
    def get(self, *args, **kwargs):
        url = self.request.get_full_path()
        lst = url.split("/")
        slug = lst[-2]
        item = Item.objects.get(slug=slug)
        items = Item.objects.filter(category=item.category)[0:4]
        items1 = Item.objects.filter(category=item.category)[5:9]
        reviews = Reviews.objects.filter(item=item) 
        review_imgs = ReviewsImage.objects.filter(item=item)
        context={'object':item,'object_list':items,'object_list1':items1, 'reviewsget':reviews, 'rimgs':review_imgs}
        try:
            context['hasdealer'] = 'yes'
            itemdealer = Itemdealer.objects.get(item=item)
            context['itemd']=itemdealer
        except:
            context['hasdealer'] = 'no'
            pass
        if len(reviews)<1:
            context['comment']="Be first to comment..."
        else:
            context['comment']=''
        return render(self.request,self.template_name,context=context)
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.method == 'POST':
                #item = get_object_or_404(Item, slug=slug)
                url = self.request.get_full_path()
                lst = url.split("/")
                slug = lst[-2]
                item = Item.objects.get(slug=slug)
                item.selcsize = self.request.POST.get("sizes_choice")
                item.save()
                try:
                    rating = self.request.POST.get("rating")
                    text = self.request.POST.get("text")
                    review = Reviews.objects.create(
                    user = self.request.user,
                    item = item,
                    review=text)
                    try:
                        review.rating = str(rating)
                        images = self.request.FILES.getlist("imgs")                        
                        for image in images:
                            rimg = ReviewsImage.objects.create(post=review,images=image,item=item)
                        review.save()
                    except:
                        pass
                except:
                    pass
                if self.request.POST.get("sizes_choice")!=None:
                    messages.info(self.request, "This item is selected with sSize "+str(item.selcsize))
                items = Item.objects.filter(category=item.category)[0:4]
                items1 = Item.objects.filter(category=item.category)[5:9]
                reviews = Reviews.objects.filter(item=item)
                review_imgs = ReviewsImage.objects.filter(item=item)
                context={'object':item,'object_list':items,'object_list1':items1, 'reviewsget':reviews, 'rimgs':review_imgs}
                try:
                    context['hasdealer'] = 'yes'
                    itemdealer = Itemdealer.objects.get(item=item)
                    context['itemd']=itemdealer
                except:
                    context['hasdealer'] = 'no'
                pass
                if len(reviews)<1:
                    context['comment']="Be first to comment..."
                else:
                    context['comment']=''
                return render(self.request,self.template_name,context=context)
        else:
            return redirect('/accounts/login')
            
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_item.size = item.selcsize
    order_item.save()
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            if item.has_size:
                messages.info(request, "This item is selected with size "+order_item.size)
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
                
def privacy(request):
    return render(request,"privacy.html")

def returnpolicy(request):
    return render(request,"returnpolicy.html")
    
def about(request):
    mteam = Team.objects.filter(team="MARKETING")
    ateam = Team.objects.filter(team="ADMINSTRATION")
    dteam = Team.objects.filter(team="DIRECTORS")
    return render(request, "about.html", {'ateam':ateam,'mteam':mteam,'dteam':dteam})
  
class temp(View):
    template_name = "temp.html"
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.userprofile.Isclubmem:
                club_member = ClubJoin.objects.filter(user=self.request.user.userprofile)
                downliners = ClubJoin.objects.filter(refered_person=self.request.user.username)
                mn,mx=0,5
                for cm in club_member:
                    cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome + cm.bonusincome + cm.positionincome + cm.levelincome
                    if cm.level<5:
                        cm.desig = "Beginner"
                        clr = 'purple'
                    elif cm.level<12 and cm.level>=5:
                        mn,mx=5,12
                        cm.desig = "SubordianteDirector"
                        clr = 'pink'
                    elif cm.level>=12 and cm.level<25:
                        mn,mx=12,25
                        cm.desig = "ManagingDirector"
                        clr = 'yellow'
                    elif cm.level>=25 and cm.level<50:
                        mn,mx=25,50
                        cm.desig = "BronzeDirector"
                        clr = 'green'
                    elif cm.level>=50 and cm.level<90:
                        mn,mx=50,90
                        cm.desig = "SilverDirector"
                        clr = 'red'
                    else:
                        mn,mx=90,150
                        cm.desig = "GoldDirector"
                        clr = 'blue'
                    cm.save()
                    
                    nw = (cm.level-int(cm.level))*100
                for cm in downliners:
                    cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome + cm.bonusincome + cm.positionincome + cm.levelincome + cm.bonusincome + cm.positionincome + cm.levelincome
                    cm.save()
                if club_member[0].team!="False":
                    team = ClubJoin.objects.filter(team=club_member[0].team)
                    for cm in team:
                        cm.usermoney = cm.travelfund + cm.teamincome + cm.downlineincome + cm.referincome + cm.orderincome + cm.bonusincome + cm.positionincome + cm.levelincome + cm.bonusincome + cm.positionincome + cm.levelincome
                        cm.save()
                carousal = CarousalClub.objects.get(pk=1)
                carousal1 = CarousalClub.objects.all().exclude(pk=1)
                context = {
                    'club_member': club_member,
                    'downliners':downliners,
                    'citems':carousal1,
                    'item':carousal
                }
                context['min']=mn
                context['max']=mx
                context['now']=nw
                context['color']=clr
                if club_member[0].team!="False":
                      context['team']=team                
                return render(self.request,self.template_name,context=context)
            elif len(Paytm_history.objects.filter(user=self.request.user, STATUS='TXN_SUCCESS'))<1:
                return redirect('/clubpayment/')
            else:
                gtype = "hidden"
                if len(self.request.user.email)<11:
                    self.request.user.email = self.request.POST.get('email')
                    gtype = "text"
                return render(self.request,self.template_name,{'type':gtype})
        else:
            return redirect('/accounts/login')
    def post(self, *args ,**kwargs):
        if self.request.user.is_authenticated:
            if not self.request.user.userprofile.Isclubmem:
                if self.request.method == 'POST':
                    if len(self.request.user.email)<11:
                        self.request.user.email = self.request.POST.get('email')
                        
                    self.request.user.userprofile.userphoto = self.request.FILES.get('image')
                    if (len(self.request.POST.get('userphonenumber'))>9 and len(self.request.POST.get('userphonenumber'))<20): 
                        self.request.user.userprofile.phone_number = self.request.POST.get('userphonenumber')
                    else:
                        messages.info(self.request, "Enter a valid Phone number")
                        return redirect('core:club')
                    self.request.user.userprofile.Isclubmem = True
                    k = refgenrator('any')
                    while len(ClubJoin.objects.filter(refer = k))>1:
                        k = refgenrator('any')
                    if not self.request.POST.get('checkbox'):
                        messages.warning(self.request, "Check the box down...")
                        return redirect('core:club')
                    if (len(self.request.POST.get('acno'))>0 and len(self.request.POST.get('ifsc'))>0) or len(self.request.POST.get('paytm'))>0: 
                        if (len(self.request.POST.get('acno'))>0 and len(self.request.POST.get('ifsc'))>0):
                            club_member = ClubJoin.objects.create(
                                user = self.request.user.userprofile,
                                refer = k,
                            )
                            club_member.Acno = self.request.POST.get('acno')
                            club_member.Ifsc = self.request.POST.get('ifsc')
                        else:
                            club_member = ClubJoin.objects.create(
                                user = self.request.user.userprofile,
                                refer = k,
                            )
                            club_member.paytm = self.request.POST.get('paytm')
                    else:
                        messages.info(self.request, "Enter valid Account number and IFSC code or Paytm number")
                        return redirect('core:club')
                    ref = self.request.POST.get('referalcode')
                    if len(ref)>0:
                        try:
                            referer = ClubJoin.objects.filter(refer=ref).first()
                            referer.childern += 1
                            referer.level = referer.level+0.2
                            if referer.level == int(referer.level):
                                if int(referer.user.paid_amt) >= 500:
                                    referer.levelincome = referer.levelincome + 15
                                else:
                                    referer.levelincome = referer.levelincome + 5 
                            if (int(referer.user.paid_amt) >= 500) and int(self.request.user.userprofile.paid_amt)>=500:
                                referer.referincome = referer.referincome + 100
                            else:
                                referer.referincome = referer.referincome + 50
                            club_member.refered_person = referer.user.user.username 
                            referer.save()
                        except:
                            pass
                    club_member.save()
                    self.request.user.userprofile.save()
                    return redirect("core:home")
            elif len(Paytm_history.objects.filter(user=self.request.user, STATUS='TXN_SUCCESS'))>0:
                return redirect('/clubpayment/')
        else:
            return redirect('accounts/login')
            
    
def sitemap(request):
    return render(request, 'sitemap.xml')

def robots(request):
    return render(request, 'robots.txt')
    
class Myorders(LoginRequiredMixin, ListView):
    template_name = "myorders.html"
    def get(self, *args, **kwargs):
        myorders = Myorder.objects.filter(user=self.request.user)
        context={'myorders':myorders}
        return render(self.request,self.template_name,context=context)
        
def categories(request, slug):
    if request.method == 'GET':
        items1 = Item.objects.filter(category=slug)
        categories = Categories.objects.all()
        paginator = Paginator(items1, 12)
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)
        context = {'object_list':items, 'cat':categories}
        return render(request,'categories.html', context=context)
    if request.method == 'POST':
        if request.POST.get('search'):
            query = request.POST.get('search')
            qs = Item.objects.filter(Q(title__search=query)|Q(category__search=query)|Q(description__search=query))
            msg = 'Search results'
            paginator = Paginator(qs, 12)
            page_number = request.GET.get('page')
            qs1 = paginator.get_page(page_number)
            context = { 'sobs': qs1 , 'type':msg}
            if len(qs)<1:
                messages.info(request, "Invalid search")
                return redirect('/ecommerce/')
        else:
            min_price = int(request.POST.get('min_price'))-int(request.POST.get('min_price'))*0.1
            max_price = int(request.POST.get('max_price'))+int(request.POST.get('max_price'))*0.1
            min_dis_per = int(request.POST.get('min_dis_price'))-int(request.POST.get('min_dis_price'))*0.1
            max_dis_per = int(request.POST.get('max_dis_price'))+int(request.POST.get('max_dis_price'))*0.1
            if request.POST.get('new'):
                qs = Item.objects.filter(category=slug).filter(Q(dis_per__gte=min_dis_per)&Q(tag="New")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
            if request.POST.get('bestseller'):
                qs = Item.objects.filter(category=slug).filter(Q(dis_per__gte=min_dis_per)&Q(tag="BESTSELLER")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
            if request.POST.get('bestseller') and request.POST.get('new'):
                qs = Item.objects.filter(category=slug).filter(Q(dis_per__gte=min_dis_per)&Q(tag="New")&Q(tag="BESTSELLER")&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
            if not (request.POST.get('bestseller') and request.POST.get('new')):
                qs = Item.objects.filter(category=slug).filter(Q(dis_per__gte=min_dis_per)&Q(dis_per__lte=max_dis_per)&Q(discount_price__gte=min_price)&Q(discount_price__lte=max_price)).order_by('-id')
            if request.POST.get('htl'):
                qs = qs.order_by('-discount_price')
            paginator = Paginator(qs, 36)
            page_number = request.GET.get('page')
            qs1 = paginator.get_page(page_number)    
            msg = 'Filter results'
            context = { 'sobs': qs1 , 'type':msg}
        return render(request, 'search.html', context=context)
    

@login_required
def refund(request, slug):
    myorderitem = get_object_or_404(Item, slug=slug)
    myorders = Myorder.objects.get(user=request.user, item=myorderitem, status='404')
    myorders.status = '200'
    myorders.save()
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi') 
    msg = EmailMessage()
    recipients = ['hemanthraju9966@gmail.com', 'navi87362@gmail.com']
    msg.set_content("This is a computer generated email, don't reply to this mail.\n"+ str(request.user.username) +" has request refund for item with name" + str(myorderitem.title) + "and amount with shippping charges Rs. "+str(myorderitem.schargeinc))
    msg['Subject'] = 'Order Cancellation'
    msg['From'] = "presimaxinfo@gmail.com"
    msg['To'] = ", ".join(recipients)
    server.send_message(msg)
    msg1 = EmailMessage()
    msg1.set_content("This is a computer generated email, don't reply to this mail.\n This mail is to confirm your order cancellation for "+  str(myorderitem.title)+" on PRESIMAX of Rs." + str(myorderitem.schargeinc) + " \nIf you want refund then please contact to +91 94932 59030 else refund is not processed.")
    msg1['Subject'] = 'Order Cancellation'
    msg1['From'] = "presimaxinfo@gmail.com"
    msg1['To'] = request.user.email
    server.send_message(msg1)
    server.quit()
    return redirect("core:myorders")

class Profile(LoginRequiredMixin, View):
    template_name = "profile.html"
    def get(self, *args, **kwargs):
        club_member = ClubJoin.objects.get(user=self.request.user.userprofile)
        context={'club_member':club_member}
        return render(self.request,self.template_name,context=context)
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            club_member = ClubJoin.objects.get(user=self.request.user.userprofile)
            if self.request.FILES.get('image'):
                self.request.user.userprofile.userphoto = self.request.FILES.get('image')
            if (len(self.request.POST.get('userphonenumber'))>9 and len(self.request.POST.get('userphonenumber'))<20): 
                self.request.user.userprofile.phone_number = self.request.POST.get('userphonenumber')
            if len(self.request.POST.get('username'))>0:
                self.request.user.username = self.request.POST.get('username')
                self.request.user.save()
            if len(self.request.user.email)>0:
                self.request.user.email = self.request.POST.get('email')
                self.request.user.save()
            self.request.user.userprofile.save()
            context={'club_member':club_member}
            return render(self.request,self.template_name,context=context)

def test(request):
    cjs = ClubJoin.objects.filter(fund_transfered=True)
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi')
    for i in cjs: 
        i.usermoney = i.travelfund + i.teamincome + i.downlineincome + i.referincome + i.orderincome + i.bonusincome + i.positionincome + i.levelincome
        msg = EmailMessage()    
        msg.set_content("This is a computer generated email, don't reply to this mail.\nMr./Mrs. "+ str(i.user.user.username).capitalize()  +", Your usermoney in Presimax Club has been deposited Rs. "+ str(i.usermoney) +" in your account.\nIf not please contact +91 9515416221.")
        msg['Subject'] = 'Fund Deposited'
        msg['From'] = "presimaxinfo@gmail.com"
        msg['To'] =  i.user.user.email
        server.send_message(msg)
        server.quit()
        i.fund_transfered = False
        i.travelfund = 0 
        i.teamincome = 0  
        i.downlineincome = 0 
        i.referincome = 0
        i.orderincome = 0 
        i.bonusincome = 0
        i.positionincome = 0 
        i.levelincome = 0
        i.usermoney = i.travelfund + i.teamincome + i.downlineincome + i.referincome + i.orderincome + i.bonusincome + i.positionincome + i.levelincome
        i.save()
    return render(request, "similarprod.html")

def faqs(request):
    faqs= FAQs.objects.all()
    context={'faq':faqs}
    return render(request, "faqs.html", context)

def push(request):
    return render(request, "sw.js")
    
def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        contactform = Contact.objects.create(name=name,email=email,subject=subject)
        contactform.subject = subject
        contactform.message = message
        contactform.save()  
        msg="Your complaint is submitted."
    return render(request, "contact.html", {'msg':msg})

def refreshprod(request):
    qs = Item.objects.filter(dis_per__lte=1)
    for i in qs:
        i.dis_per = ((i.price - i.club_discount_price)/i.price)*100
        i.club_discount_price = int(i.discount_price*0.9)
        i.save()
    for i in qs:
        if i.discount_price:
            if i.pweight <= 0.5:
                i.schargeinc=i.discount_price+57
                i.club_schargeinc=i.club_discount_price+57
            elif i.pweight <= 1 and i.pweight>0.5:
                i.schargeinc=i.discount_price+72
                i.club_schargeinc=i.club_discount_price+72
            elif i.pweight>1:
                if (i.pweight) != int(i.pweight):
                    i.schargeinc=i.discount_price+72+int(i.pweight+1)*66
                    i.club_schargeinc=i.club_discount_price+72+int(i.pweight+1)*66
                else:
                    i.schargeinc=i.discount_price+72+int(i.pweight)*66
                    i.club_schargeinc=i.club_discount_price+72+int(i.pweight)*66
            i.save()
    return render(request, "refreshhome.html")

def error_404(request, exception):
        data = {}
        return render(request,'404error.html', data)

def error_500(request,  exception):
        data = {}
        return render(request,'404error.html', data)
        
def error_413(request,  exception):
        data = {}
        return render(request,'404error.html', data)        
