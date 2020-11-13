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
from .forms import CheckoutForm, CouponForm, RefundForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile, Transaction, TravelDetails, ClubJoin, Paytm_order_history,Paytm_history, Carousal, Review, Team, Ads, Itemdealer, Myorder, Categories, Sales, CarousalClub, Contact, FAQs, CarousalEcommerce,Multiple_Pics, Productbackground, Pagebackground, Extrasales, Withdraw
import random
from django.shortcuts import reverse
import string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
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

def send_email(sub,des,to_user):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi')
        msg1 = EmailMessage()
        msg1.set_content(des)
        msg1['Subject'] = sub
        msg1['From'] = "presimaxinfo@gmail.com"
        msg1['To'] = to_user
        server.send_message(msg1)
        server.quit()
    except:
        pass
    return True
   
def distribute_money(request,amt):
    try:        
        amt = float(amt)
        up = request.user.userprofile        
        cm = ClubJoin.objects.get(user=up)
        new_level = float(cm.level) + round(amt/3000,1)        
        if int(cm.user.paid_amt) >= 500: 
            cm.orderincome = float(cm.orderincome)+(amt)*0.1
            cm.save()
        else:
            cm.orderincome = float(cm.orderincome)+(amt)*0.05
            cm.save()        
        cm.level = new_level
        cm.save()
        if cm.referer:             
            ref = ClubJoin.objects.get(user=cm.referer)
            if int(cm.referer.paid_amt) >= 500:                  
                ref.downlineincome = float(ref.downlineincome) + (amt)*0.01
            else:
                ref.downlineincome = float(ref.downlineincome) + (amt)*0.007
            ref.save()
    except:
        messages.info(request,'Unable to add bonus to your wallet, please contact us')    

def collect_money(request,amt):
    try:        
        amt = float(amt)
        up = request.user.userprofile        
        cm = ClubJoin.objects.get(user=up)      
        if int(cm.user.paid_amt) >= 500: 
            cm.orderincome = float(cm.orderincome)-(amt)*0.1
            cm.save()
        else:
            cm.orderincome = float(cm.orderincome)-(amt)*0.05
            cm.save()        
        if cm.referer:                       
            ref = ClubJoin.objects.get(user=cm.referer)
            if int(cm.referer.paid_amt) >= 500:                    
                ref.downlineincome = float(ref.downlineincome) - (amt)*0.01
            else:
                ref.downlineincome = float(ref.downlineincome) - (amt)*0.007
            ref.save()
    except:
        messages.info(request,'Unable to add bonus to your wallet, please contact us')  
  
def brokrage_income(request,orderitem): 
    up = get_object_or_404(UserProfile,user=orderitem.referer)
    cp = get_object_or_404(ClubJoin,user=up)
    dp = float(orderitem.item.discount_price)
    if dp>199 and dp<401:
        add=25
    elif dp>400 and dp<901:
        add=40
    elif dp>900 and dp<1901:
        add=50
    if dp>1900 and dp<4001:
        add=75
    else:
        add=100
    cp.prod_ref_inc = float(cp.prod_ref_inc)+add
    cp.save()
    sub = 'Product refer income | Presimax'    
    des = "This is a computer generated email don't reply to this mail.\n This mail is to inform you that you are acknowledged with Rs." + str(add) + "  for refering. Visit us again."                    
    send_email(sub,des,str(request.user.email))    

def de_brokrage_income(request,orderitem): 
    up = get_object_or_404(UserProfile,user=orderitem.referer)
    cp = get_object_or_404(ClubJoin,user=up)
    dp = float(orderitem.item.discount_price)
    if dp>199 and dp<401:
        add=25
    elif dp>400 and dp<901:
        add=40 
    elif dp>900 and dp<1901:
        add=50
    if dp>1900 and dp<4001:
        add=75
    else:
        add=100
    cp.prod_ref_inc = float(cp.prod_ref_inc)-add
    cp.save()  

def is_valid_form(values): 
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False).last()
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            context['COD_avail'] = 'YES'            
            for o in order.items.all():
                if not o.item.COD:
                    context['COD_avail'] = 'NO'
                    messages.info(self.request, "All products in your order doesn't avail cash on delivery facility.")
                        
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
            order = Order.objects.filter(user=self.request.user, ordered=False).last()
            if form.is_valid() or True:
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
                    order.payment = payment_option
                    order.save()
                    return redirect('core:orderpayment')
                if payment_option == 'C':                                        
                    for o in order.items.all():
                        if not o.item.COD:                              
                            messages.warning(self.request, "All products in your order doesn't avail cash on delivery facility.")          
                            return redirect('core:checkout')     
                    order.payment = payment_option
                    order.save()                                                  
                    return redirect('core:orderplaced')                      
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')            
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")
          

@login_required
def orderplaced(request):
    order = Order.objects.filter(user=request.user, ordered=False).last()     
    amt = order.get_total() 
    transaction = Transaction.objects.create(made_by=request.user, amount=amt)
    transaction.save()
    sub = 'Order Successfully Placed | Presimax'    
    des = "This is a computer generated email don't reply to this mail.\n This mail is to confirm your order on PRESIMAX of Rs." + str(amt) + " with order Id "+ str(transaction.order_id) + " by "+ str(request.user.username) +".\nThank you for purchasing. Visit us again."                    
    send_email(sub,des,str(request.user.email)) 
    oitms = order.items.all()    
    for i in oitms:
        i.ordered = True
        if i.referer:
            brokrage_income(request,i)
        myorder = Myorder.objects.create(user=request.user,item=i.item,myordered_date=datetime.now(),mydelivery_date=datetime.now()+timedelta(days=5))
        myorder.orderitem = i
        myorder.save()
        i.save()  
    distribute_money(request,amt=amt)
    order.ordered = True
    order.save()    
    resp = '''<center><img style='width:80%;height:auto' src="https://www.presimax.online/media/images/ezgif.com-gif-maker_1.gif"></center>'''
    return HttpResponse(resp)
        

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
    order = Order.objects.filter(user=request.user, ordered=False).last()
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
                try:
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
                except:
                    pass
                msg = "PS"
            else:
                try:
                    msg = EmailMessage()
                    msg.set_content("This is a computer generated email don't reply to this mail.\n This mail is to report your entry attempt to our club has failed. Join to our club to enjoy our services.")
                    msg['Subject'] = 'Presimax-online shopping and money earning'
                    msg['From'] = "presimaxinfo@gmail.com"
                    msg['To'] = cust.email
                    server.send_message(msg)
                    server.quit()
                except:
                    pass
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
                    try:
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
                    except:
                        pass
                order = Order.objects.filter(user=cust, ordered=False).last()
                qs = order.items.all()
                amt = data_dict["TXNAMOUNT"]
                oitms = qs
                for i in oitms:
                    i.ordered = True
                    brokrage_income(request,i)
                    myorder = Myorder.objects.create(user=cust,item=i.item,myordered_date=datetime.now(),mydelivery_date=datetime.now()+timedelta(days=5))
                    myorder.orderitem = i
                    myorder.save()
                    i.save()
                order.ordered = True
                order.save()
                up = UserProfile.objects.get(user=cust)
                cm = ClubJoin.objects.get(user=up)
                distribute_money(request,amt)
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

CATEGORYCHOICES = {'H': 'handi crafts','SS': 'sarees','G': 'grocery','P':'daily Needs','FW': 'fashion wear','F': 'foot wear','FU': 'furniture','MW': 'menswear','BC': 'beauty care','E': 'electronics','MA': 'mens accessories','WA': 'womens accessories','MP':'mobiles & accessories','HA': 'home appliances','S': 'sports','HC': 'health','KW': 'kids wear','B': 'books','AA': 'auto accessories','J':'jewellery'}  
CATEGORYCHOICES = {value : key for (key, value) in CATEGORYCHOICES.items()}
def get_model_or_nothing(model_name):
    try:        
        return model_name.objects.all()
    except:
        return False

class HomeView(ListView):
    template_name = "home.html"
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated: 
            buynows = Order.objects.filter(user=self.request.user, ordered=False,type='BN')
            buynows.delete()
        sword = self.request.GET.get('search', False)
        catgeory = self.request.GET.get('category', False)
        if sword:
            qs = Item.objects.filter(Q(title__search=sword)|Q(category__search=sword)|Q(description__search=sword))
            if catgeory and catgeory!='All':
                cchoice = CATEGORYCHOICES[catgeory.lower().strip()]
                qs = qs.filter(category=cchoice)
            return render(self.request, 'search.html', context={'sobs': qs, 'type': 'Search Results for word - '+sword})            
        items = Item.objects.all().order_by('-id')[0:12]
        items4 = Sales.objects.filter(sale_name="GDO")
        items7 = Item.objects.filter(tag="BESTSELLER").order_by('-id')[0:16]
        items8 = Sales.objects.filter(sale_name="DOW")
        items11 = Sales.objects.filter(sale_name="DS")
        items9 = Sales.objects.filter(sale_name="DOD")
        items10 = Sales.objects.filter(sale_name="FO")
        categories = Categories.objects.all()
        context={'object_list':items,'cat':categories,'great_discounts':items4,'Bestsellers':items7,'Deals_of_week':items8,'deals_of_day':items9,'flash_sale':items10,'sunday_sale':items11,'time':timezone.now()}
        context['sp1_s'],context['sp2_s'],context['sp3_s'] = False,False,False
        try:
            sp1 = Extrasales.objects.all()[0]
            context['sp1'] = sp1
            context['sp1_s'],context['sp2_s'],context['sp3_s'] = True,False,False
        except:
            pass
        try:
            sp2 = Extrasales.objects.all()[1]
            context['sp2'] = sp2
            context['sp1_s'],context['sp2_s'],context['sp3_s'] = True,True,False
        except:
            pass
        try:
            sp3 = Extrasales.objects.all()[2]
            context['sp3'] = sp3
            context['sp1_s'],context['sp2_s'],context['sp3_s'] = True,True,True
        except:
            pass
        posters = get_model_or_nothing(Ads)
        context['poster'] = posters.order_by('id')
        ctop = CarousalEcommerce.objects.all()
        context['ctop']=ctop
        context["sunday_status"]=False
        if datetime.now().strftime("%A")=="Monday":            
            context["sunday_status"]=True                        
        if items11:
            context["sunday_status"]=True
        else:
            context["sunday_status"]=False
        now = timezone.now()
        try:
            if len(items10)>0:
                sdate = items10[0].start
                edate = items10[0].end
                today = datetime.today()
                if now > edate:
                    context["day"]=now.day
                    context["hours"]=now.hour 
                    context["minutes"]=now.minute
                    context["seconds"]=now.second                    
                elif sdate < now:
                    context["day"]=edate.day - now.day
                    context["hours"]=edate.hour
                    context["minutes"]=edate.minute
                    context["seconds"]=edate.second                                    
                else:
                    context["day"]=-sdate.day + now.day
                    context["hours"]=sdate.hour
                    context["minutes"]=sdate.minute
                    context["seconds"]=sdate.second
                context['fsale']=True                   
                if sdate > now or now > edate:
                    context['fsale']=False
                    context["fstatus"]="disabled"
        except:
            pass
        try:
          bbi = Pagebackground.objects.filter(page="H").order_by('-id')[0]
          context['bbi']=bbi          
        except:
            pass 
        try:
          pbc = Productbackground.objects.filter(page="H").order_by('-id')[0]
          context['pbc']=pbc                            
        except:
            pass
        resp = render(self.request, self.template_name, context) 
        resp.set_cookie(key='seen', value=1,expires=None)
        return resp 
    
            
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
            buynows = Order.objects.filter(user=self.request.user, ordered=False,type='BN')
            buynows.delete()
            if self.request.user.userprofile.Isclubmem:
                club_member = ClubJoin.objects.get(user=self.request.user.userprofile)
                downliners = ClubJoin.objects.filter(referer=club_member.user)                                    
                nw = (club_member.level-int(club_member.level))*100                                    
                if club_member.team!="False":
                    team = ClubJoin.objects.filter(team=club_member.team)                    
                carousal = CarousalClub.objects.get(pk=1)
                carousal1 = CarousalClub.objects.all().exclude(pk=1)
                cms = ClubJoin.objects.filter(user=self.request.user.userprofile)
                context = {
                    'club_member': cms,
                    'downliners':downliners,
                    'citems':carousal1,
                    'item':carousal
                }
                context['now']=nw
                if club_member.team!="False":
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
            return redirect('/accounts/login/')
    def post(self, *args ,**kwargs):
        if self.request.user.is_authenticated:
            if not self.request.user.userprofile.Isclubmem:
                if self.request.method == 'POST':
                    self.request.user.userprofile.userphoto = self.request.FILES.get('image')
                    if (len(self.request.POST.get('userphonenumber'))>9 and len(self.request.POST.get('userphonenumber'))<20): 
                        self.request.user.userprofile.phone_number = self.request.POST.get('userphonenumber')
                    else:
                        messages.info(self.request, "Enter a valid Phone number")
                        return redirect('core:club')
                    self.request.user.userprofile.Isclubmem = True
                    k = refgenrator('any')
                    try:
                        while len(ClubJoin.objects.filter(refer = k))>1:
                            k = refgenrator('any')
                    except:
                        pass
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
                            if (int(referer.user.paid_amt) >= 500) and int(self.request.user.userprofile.paid_amt)>=500:
                                referer.referincome = referer.referincome + 100
                            else:
                                referer.referincome = referer.referincome + 50
                            club_member.referer = referer.user
                            referer.save()
                        except:
                            pass
                    if int(self.request.user.userprofile.paid_amt)>=500:
                        club_member.premium = True
                    club_member.save()
                    self.request.user.userprofile.save()
                    return redirect("core:club")
            elif len(Paytm_history.objects.filter(user=self.request.user, STATUS='TXN_SUCCESS'))>0:
                return redirect('/clubpayment/')
        else:
            return redirect('/accounts/login/')
            
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
            order = Order.objects.filter(user=self.request.user, ordered=False).last()
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/ecommerce/")
            

class ItemDetailView(View):
    template_name = "product.html"
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated: 
            buynows = Order.objects.filter(user=self.request.user, ordered=False,type='BN')
            buynows.delete()        
        item = Item.objects.get(slug=self.kwargs['slug'])       
        reviews = Review.objects.filter(item=item)                     
        context={'object':item,'reviews':reviews}       
        context['referid'] = '0'        
        if 'refer-product' in str(self.request.path).split('/'):
            context['referid'] = self.kwargs['referid']
        try:
            context['hasdealer'] = 'yes'
            itemdealer = Itemdealer.objects.get(item=item)
            context['itemd']=itemdealer
        except:
            context['hasdealer'] = 'no'
            pass        
        return render(self.request,self.template_name,context=context)

def review_count(item):
    qs = Review.objects.filter(item=item)
    if qs.exists():
        return len(qs)
    return 0          
            
@login_required            
def reviewform(request,slug,userid):
    item = get_object_or_404(Item, slug=slug)
    user = get_object_or_404(User,pk=userid)
    try:
        rating = request.POST.get("rating")
        text = request.POST.get("text")
        item.rating = (float(item.rating)+float(rating))/(review_count(item)+1)
        item.save()
        review = Review.objects.create(user = user,item = item,review=text)
        review.rating = str(rating)
        review.save()
        try:
            images = request.FILES.getlist("imgs")
            i=0                        
            for image in images:                
                name = 'rp'+str(i)+str(user.username)+text[:6]
                i+=1
                rimg = Multiple_Pics.objects.create(image=image,name=name)
                review.images.add(rimg)
            review.save()
        except:
            pass
    except:
            pass
    return redirect("core:product", slug=slug)


@login_required
def add_to_cart(request, slug, referid=None):
    item = get_object_or_404(Item, slug=slug)
    selcsize = request.POST.get("size", False)
    qty = request.POST.get("quantity", False)
    if item.has_size:
        if not selcsize:
            messages.info(request, " Select product size ")
            return redirect("core:product", slug=slug)
    if qty:
        qty = int(qty)
    if selcsize:
        order_item, created = OrderItem.objects.get_or_create(
            item=item, user=request.user, ordered=False, size=selcsize)
    else:
        order_item, created = OrderItem.objects.get_or_create(
            item=item, user=request.user, ordered=False)
    try:
        referer = User.objects.get(pk=referid)
        if request.user != referer:
            order_item.referer = referer
            order_item.save()
        else:
            messages.warning(request, "You can't refer yourself.")
    except:
        pass
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.type != 'BN':
            try:
                buynows = Order.objects.filter(
                    user=request.user, ordered=False, type='BN')
                buynows.delete()
            except:
                pass
        if selcsize:
            check_order = order.items.filter(
                item__slug=item.slug, size=selcsize)
        else:
            check_order = order.items.filter(item__slug=item.slug)
        if referid:
            if selcsize:
                check_order = order.items.filter(
                    item__slug=item.slug, size=selcsize)
            else:
                check_order = order.items.filter(item__slug=item.slug)
        if check_order.exists():
            if qty:
                order_item.quantity = qty
            else:
                order_item.quantity += 1
            if selcsize:
                order_item.size = selcsize
            order_item.save()
            if item.has_size:
                messages.info(
                    request, "This item is selected with size "+order_item.size)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            if qty:
                order_item.quantity = qty
                order_item.save()
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date, type='S')
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def buy_now(request, slug, referid=None):
    item = get_object_or_404(Item, slug=slug)
    selcsize = request.POST.get("size", False)
    qty = request.POST.get("quantity", False)
    if item.has_size:
        if not selcsize:
            messages.info(request, " Select product size ")
            return redirect("core:product", slug=slug)
    if qty:
        qty = int(qty)
    if selcsize:
        order_item, created = OrderItem.objects.get_or_create(
            item=item, user=request.user, ordered=False, size=selcsize)
    else:
        order_item, created = OrderItem.objects.get_or_create(
            item=item, user=request.user, ordered=False)
    try:
        referer = User.objects.get(pk=referid)
        if request.user != referer:
            order_item.referer = referer
            order_item.save()
        else:
            messages.warning(request, "You can't refer yourself.")
    except:
        pass
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.type != 'BN':
            try:
                buynows = Order.objects.filter(
                    user=request.user, ordered=False, type='BN')
                buynows.delete()
            except:
                pass
        if selcsize:
            check_order = order.items.filter(
                item__slug=item.slug, size=selcsize)
        else:
            check_order = order.items.filter(item__slug=item.slug)
        if referid:
            if selcsize:
                check_order = order.items.filter(
                    item__slug=item.slug, size=selcsize)
            else:
                check_order = order.items.filter(item__slug=item.slug)
        if check_order.exists():
            if qty:
                order_item.quantity = qty
            else:
                order_item.quantity += 1
            if selcsize:
                order_item.size = selcsize
            order_item.save()
            if item.has_size:
                messages.info(
                    request, "This item is selected with size "+order_item.size)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            if qty:
                order_item.quantity = qty
                order_item.save()
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    ordered_date = timezone.now()
    order = Order.objects.create(
        user=request.user, ordered_date=ordered_date, type='BN')
    order.items.add(order_item)
    return redirect("core:order-summary")     

@login_required
def remove_from_cart(request, slug,referid=None):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
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
def remove_single_item_from_cart(request, slug,referid=None):
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
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated: 
            buynows = Order.objects.filter(user=self.request.user, ordered=False,type='BN')
            buynows.delete()
        sword = self.request.GET.get('search', False)
        catgeory = self.request.GET.get('category', False)
        if sword:
            qs = Item.objects.filter(Q(title__search=sword)|Q(category__search=sword)|Q(description__search=sword))
            if catgeory and catgeory!='All':
                cchoice = CATEGORYCHOICES[catgeory.lower().strip()]
                qs = qs.filter(category=cchoice)
            return render(self.request, 'search.html', context={'sobs': qs , 'type':'Search Results for word'+sword})
        items = Item.objects.all().order_by('-id')[0:12]
        items4 = Item.objects.filter(dis_per__gte=70).order_by('-id')
        items7 = Item.objects.filter(tag="BESTSELLER").order_by('-id')[0:16]
        items8 = Sales.objects.filter(sale_name="DOW").order_by('-id')
        items11 = Sales.objects.filter(sale_name="DS")
        items9 = Sales.objects.filter(sale_name="DOD")
        items10 = Sales.objects.filter(sale_name="FO")
        categories = Categories.objects.all()
        context={'object_list':items,'cat':categories,'great_discounts':items4,'Bestsellers':items7,'Deals_of_week':items8,'deals_of_day':items9,'flash_sale':items10,'sunday_sale':items11,'time':timezone.now()}
        context['sp1_s'],context['sp2_s'],context['sp3_s'] = False,False,False
        try:
            sp1 = Extrasales.objects.all()[0]
            context['sp1'] = sp1
        except:
            pass
        try:
            sp2 = Extrasales.objects.all()[1]
            context['sp2'] = sp2
        except:
            pass
        try:
            sp3 = Extrasales.objects.all()[2]
            context['sp3'] = sp3
        except:
            pass
        posters = get_model_or_nothing(Ads)
        context['poster'] = posters
        ctop = CarousalEcommerce.objects.all()
        context['ctop']=ctop
        context["sunday_status"]=False
        if datetime.now().strftime("%A")=="Sunday":            
            context["sunday_status"]=True            
        now = timezone.now()
        try:
            if len(items10)>0:
                sdate = items10.start
                edate = items10.end
                today = datetime.today()
                if sdate < now:
                    context["day"]=edate.day - now.day
                    context["hours"]=edate.hour
                    context["minutes"]=edate.minute
                    context["seconds"]=edate.second
                    context['fsale']=False
                elif now > edate:
                    context["day"]=now.day
                    context["hours"]=now.hour 
                    context["minutes"]=now.minute
                    context["seconds"]=now.second
                    context['fsale']=False
                else:
                    context["day"]=-sdate.day + now.day
                    context["hours"]=sdate.hour
                    context["minutes"]=sdate.minute
                    context["seconds"]=sdate.second
                    context['fsale']=True
                if sdate > now or now > edate:
                    context["fstatus"]="disabled"
        except:
            pass
        try:
          bbi = Pagebackground.objects.all().order_by('-id')[0]
          context['bbi']=bbi          
        except:
            pass 
        try:
          pbc = Productbackground.objects.all().order_by('-id')[0]
          context['pbc']=pbc                            
        except:
            pass 
        return render(self.request, self.template_name, context)
        
    
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

# changed
def categories(request, slug):
    if request.method == 'GET':
        sword = request.GET.get('search', False)
        items1 = Item.objects.filter(category=slug)
        categories = Categories.objects.all()
        paginator = Paginator(items1, 12)
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)
        context = {'object_list': items, 'cat': categories}
        if sword:
            qs = Item.objects.filter(Q(title__search=sword) | Q(
                category__search=sword) | Q(description__search=sword))            
            if qs.count() < 1:
                messages.info(request, 'No results for your search '+sword)
                return render(request, 'sales.html', context=context)
            return render(request, 'search.html', context={'sobs': qs, 'type': 'Search Results for word - '+sword})
        try:
          bbi = Pagebackground.objects.filter(page="C").order_by('-id')[0]
          context['bbi']=bbi          
        except:
            pass 
        try:
          pbc = Productbackground.objects.filter(page="C").order_by('-id')[0]
          context['pbc']=pbc                            
        except:
            pass
        context['action'] = reverse('core:category_search',kwargs={'slug':slug})
        return render(request, 'categories.html', context=context)                

# changed
def search(request, slug=None):
    if request.method == 'GET':
        qs = Item.objects.all().order_by('-id')
        if slug:
            qs = qs.filter(category=slug)
        if int(request.GET.get('max_price')) - int(request.GET.get('min_price')) > 3:
            min_price = int(request.GET.get('min_price')) - \
                int(request.GET.get('min_price'))*0.05     
            max_price = int(request.GET.get('max_price')) + \
                int(request.GET.get('max_price'))*0.05
            qs = qs.filter(Q(discount_price__gte=min_price) & Q(discount_price__lte=max_price))
        if int(request.GET.get('max_dis_price')) - int(request.GET.get('min_dis_price')) > 3:
            min_dis_per = int(request.GET.get('min_dis_price')) - \
                int(request.GET.get('min_dis_price'))*0.05
            max_dis_per = int(request.GET.get('min_dis_price')) + \
                int(request.GET.get('max_dis_price'))*0.05
            qs = qs.filter(Q(dis_per__gte=min_dis_per) & Q(dis_per__lte=max_dis_per))
        if request.GET.get('new'):
            qs = qs.filter(tag="New")
        if request.GET.get('bestseller'):
            qs = qs.filter(tag="BESTSELLER")        
        if request.GET.get('htl'):
            qs = qs.order_by('-discount_price')
        paginator = Paginator(qs, 12)
        page_number = request.GET.get('page')
        qs1 = paginator.get_page(page_number)
        msg = 'Filter results'
        context = {'sobs': qs1, 'type': msg}
        try:
          bbi = Pagebackground.objects.filter(page="C").order_by('-id')[0]
          context['bbi']=bbi          
        except:
            pass 
        try:
          pbc = Productbackground.objects.filter(page="C").order_by('-id')[0]
          context['pbc']=pbc                            
        except:
            pass        
        return render(request, 'search.html', context=context)

# changed
def sales(request, slug):
    if request.method == 'GET':
        sword = request.GET.get('search', False)                        
        items1 = Sales.objects.filter(sale_name=slug)[0]
        categories = Categories.objects.all()
        itemsx = items1.item.all()
        paginator = Paginator(itemsx, 12)
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)
        items.sale_name = items1.get_sale_name_display()
        context = {'object_list': items, 'cat': categories}
        if sword:
            qs = Item.objects.filter(Q(title__search=sword) | Q(
                category__search=sword) | Q(description__search=sword))            
            if qs.count() < 1:
                messages.info(request, 'No results for your search '+sword)
                return render(request, 'sales.html', context=context)
            return render(request, 'search.html', context={'sobs': qs, 'type': 'Search Results for word - '+sword})
        try:
          bbi = Pagebackground.objects.filter(page="C").order_by('-id')[0]
          context['bbi']=bbi          
        except:
            pass 
        try:
          pbc = Productbackground.objects.filter(page="C").order_by('-id')[0]
          context['pbc']=pbc                            
        except:
            pass
        context['action'] = reverse('core:search_sales',kwargs={'slug':slug})
        return render(request, 'sales.html', context=context)

def Xtrasales(request, slug):
    if request.method == 'GET':
        sword = request.GET.get('search', False)                        
        items1 = Extrasales.objects.filter(sale_name=slug)[0]
        categories = Categories.objects.all()
        itemsx = items1.item.all()
        paginator = Paginator(itemsx, 12)
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)
        items.sale_name = items1.sale_name
        context = {'object_list': items, 'cat': categories}
        if sword:
            qs = Item.objects.filter(Q(title__search=sword) | Q(
                category__search=sword) | Q(description__search=sword))            
            if qs.count() < 1:
                messages.info(request, 'No results for your search '+sword)
                return render(request, 'sales.html', context=context)
            return render(request, 'search.html', context={'sobs': qs, 'type': 'Search Results for word - '+sword})
        try:
          bbi = Pagebackground.objects.filter(page="C").order_by('-id')[0]
          context['bbi']=bbi          
        except:
            pass 
        try:
          pbc = Productbackground.objects.filter(page="C").order_by('-id')[0]
          context['pbc']=pbc                            
        except:
            pass
        context['action'] = reverse('core:search_xtrasales',kwargs={'slug':slug})
        return render(request, 'sales.html', context=context)    

def search_xtrasales(request, slug):
    search_sales(request, slug, model=Extrasales)

# changed
def search_sales(request, slug, model=Sales):
    if request.method == 'GET':
        qs = model.objects.filter(sale_name=slug)[0].item.all().order_by('-id')
        if int(request.POST.get('max_price')) - int(request.GET.get('min_price')) > 3:
            min_price = int(request.GET.get('min_price')) - \
                int(request.GET.get('min_price'))*0.05     
            max_price = int(request.GET.get('max_price')) + \
                int(request.GET.get('max_price'))*0.05
            qs = qs.filter(Q(discount_price__gte=min_price) & Q(discount_price__lte=max_price))
        if int(request.GET.get('max_dis_price')) - int(request.POST.get('min_dis_price')) > 3:
            min_dis_per = int(request.GET.get('min_dis_price')) - \
                int(request.GET.get('min_dis_price'))*0.05
            max_dis_per = int(request.POST.get('min_dis_price')) + \
                int(request.GET.get('max_dis_price'))*0.05
            qs = qs.filter(Q(dis_per__gte=min_dis_per) & Q(dis_per__lte=max_dis_per))
        if request.GET.get('new'):
            qs = qs.filter(tag="New")
        if request.GET.get('bestseller'):
            qs = qs.filter(tag="BESTSELLER")        
        if request.GET.get('htl'):
            qs = qs.order_by('-discount_price')
        paginator = Paginator(qs, 12)
        page_number = request.GET.get('page')
        qs1 = paginator.get_page(page_number)
        msg = 'Filter results'
        context = {'sobs': qs1, 'type': msg}
        try:
          bbi = Pagebackground.objects.filter(page="C").order_by('-id')[0]
          context['bbi']=bbi          
        except:
            pass 
        try:
          pbc = Productbackground.objects.filter(page="C").order_by('-id')[0]
          context['pbc']=pbc                            
        except:
            pass        
        return render(request, 'search.html', context=context)        

@login_required
def withdraw(request):
    if request.method == "GET":
        return render(request,'withdraw.html')
    if request.method == "POST":
        amt = float(request.POST.get('amt'))
        n = 0
        try:
            wds = Withdraw.objects.filter(user=request.user.userprofile).filter(at__gte=datetime.now()-timedelta(days=1))
            n = wds.count()
        except:
            pass        
        if float(request.user.userprofile.clubjoin.usermoney)>=amt and n < 1:            
            if amt >=50 and amt <= 500:
                Withdraw.objects.create(user=request.user.userprofile,amount=amt)
                messages.info(request,'Request is sent.')
                return redirect('core:Profile')
            else:
                messages.warning(request,'Amount should be in given range.')
        else:
            if not float(request.user.userprofile.clubjoin.usermoney)>=amt:
                messages.warning(request,'Insufficient balance.')
            if n>=1:
                messages.warning(request,'Only one request per day.')
        return redirect('core:withdraw')        

@login_required
def refund(request, pk):    
    myorders = Myorder.objects.get(user=request.user, id=pk)
    myorderitem = myorders.item
    myorders.status = 'R'
    myorders.save()
    amt = myorders.orderitem.price_inc_ship    
    collect_money(request,amt)
    try:
        de_brokrage_income(request,myorders.orderitem)
    except:
        pass
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi') 
    msg = EmailMessage()
    recipients = ['hemanthraju9966@gmail.com', 'navi87362@gmail.com']
    msg.set_content("This is a computer generated email, don't reply to this mail.\n"+ str(request.user.username) +" has request refund for item with name" + str(myorderitem.title) + "and amount with shippping charges Rs. "+str(myorders.orderitem.price_inc_ship))
    msg['Subject'] = 'Order Cancellation'
    msg['From'] = "presimaxinfo@gmail.com"
    msg['To'] = ", ".join(recipients)
    server.send_message(msg)
    msg1 = EmailMessage()
    msg1.set_content("This is a computer generated email, don't reply to this mail.\n This mail is to confirm your order cancellation for "+  str(myorderitem.title)+" on PRESIMAX of Rs." + str(myorders.orderitem.price_inc_ship) + " \nIf you want refund then please contact to +91 94932 59030 else refund is not processed.")
    msg1['Subject'] = 'Order Cancellation'
    msg1['From'] = "presimaxinfo@gmail.com"
    msg1['To'] = request.user.email
    server.send_message(msg1)
    server.quit()
    return redirect("core:myorders")

class Profile(LoginRequiredMixin, View):
    template_name = "profile.html"
    def get(self, *args, **kwargs):
        return render(self.request,self.template_name)
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            club_member = user=self.request.user.userprofile
            if self.request.FILES.get('image'):
                self.request.user.userprofile.userphoto = self.request.FILES.get('image')
            if self.request.POST.get('userphonenumber'):
                if (len(self.request.POST.get('userphonenumber'))>9 and len(self.request.POST.get('userphonenumber'))<20): 
                    self.request.user.userprofile.phone_number = self.request.POST.get('userphonenumber')            
            if self.request.POST.get('username'):
                self.request.user.username = self.request.POST.get('username')
                self.request.user.save()
            if self.request.POST.get('email'):
                self.request.user.email = self.request.POST.get('email')
                self.request.user.save()
            self.request.user.userprofile.save()
            return redirect("core:Profile")

def test(request):
    cjs = ClubJoin.objects.filter(fund_transfered=True)
    cm = ClubJoin.objects.all()
    for i in cm:
        i.usermoney = i.travelfund + i.teamincome + i.downlineincome + i.referincome + i.orderincome + i.bonusincome + i.positionincome + i.levelincome
        i.save()
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('presimaxinfo@gmail.com','Mama_presimax_bagundi')
    for i in cjs: 
        try:
            msg = EmailMessage()    
            msg.set_content("This is a computer generated email, don't reply to this mail.\nMr./Mrs. "+ str(i.user.user.username).capitalize()  +", Your usermoney in Presimax Club has been deposited Rs. "+ str(i.usermoney) +" in your account.\nIf not please contact +91 9515416221.")
            msg['Subject'] = 'Fund Deposited'
            msg['From'] = "presimaxinfo@gmail.com"
            msg['To'] =  i.user.user.email
            server.send_message(msg)
            server.quit()
        except:
            pass
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

@login_required
def downliners(request):
    if request.method == "GET":
        if request.user.userprofile.Isclubmem:
            cjs = None            
            try:
                cjs = ClubJoin.objects.filter(referer=request.user.userprofile)
            except:
                pass            
            context = { 'object_list':cjs }
            try:
              bbi = Pagebackground.objects.filter(page="C").order_by('-id')[0]
              context['bbi']=bbi          
            except:
                pass 
            try:
              pbc = Productbackground.objects.filter(page="C").order_by('-id')[0]
              context['pbc']=pbc                            
            except:
                pass 
            return render(request, 'downliners.html',context)
                    

import json

def auto(request):
    if request.method == 'GET':
        qs = Item.objects.filter(title__icontains = request.GET.get('search'))
        ns = Item.objects.filter(title__search = request.GET.get('search'))
        qs = ns | qs
        titles = []
        for i in qs:
          t = i.title
          titles.append(t)          
        data = json.dumps(titles[:50])
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    if request.method == 'POST':
        qs = Item.objects.filter(title__icontains = request.GET.get('search'))
        ns = Item.objects.filter(title__search = request.GET.get('search'))
        qs = ns | qs
        titles = []
        for i in qs:
          t = i.title
          titles.append(t)          
        data = json.dumps(titles[:50])
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

 
def error_404(request, exception):
        data = {}
        return render(request,'404error.html', data)

def error_500(request):
        data = {}
        return render(request,'404error.html', data)
        
def error_413(request, exception):
        data = {}
        return render(request,'404error.html', data)        
