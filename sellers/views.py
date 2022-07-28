from django.http import request
from django.shortcuts import render
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
from .forms import ItemForm
from .models import SellerItem
from core.models import Multiple_Pics
from django.shortcuts import reverse
import string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from core.paytm import generate_checksum, verify_checksum
import smtplib
from django.core.paginator import Paginator
from email.message import EmailMessage
from datetime import datetime, timedelta
from django.db.models import Q

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

class AddItem(LoginRequiredMixin, View):
    template_name = "selleritem_form.html"
    def get(self,*args, **kwargs):    
        form = ItemForm()
        context = {'form':form}
        return render(self.request, self.template_name, context)
    def post(self,*args, **kwargs):
        form = ItemForm(self.request.POST or None)
        if form.is_valid() or True:
            print(form.cleaned_data.get('title'))
            item = SellerItem.objects.create(title=form.cleaned_data.get('title'), price=form.cleaned_data.get('price'), category=form.cleaned_data.get('category'), description=form.cleaned_data.get('description'),image=self.request.FILES.get('img'))
            if self.request.POST.get('sizecheck'):
                item.has_size=True
                item.size=self.request.POST.get('size')
            item.owner = self.request.user
            item.pweight=self.request.POST.get('weight')
            item.save()            
            images = self.request.FILES.getlist("imgs")
            i=0                        
            for image in images:                
                name = 'rp'+str(i)+str(self.request.user.username)+str(item.title)[:6]
                i+=1
                rimg = Multiple_Pics.objects.create(image=image, name=name)
                item.pis.add(rimg)
            item.save()   
            sub="Review A New Product - From "+str(self.request.user.username)
            des = 'Mr./Mrs. '+str(self.request.user.username)+' has added a new product in your store, Please review it.'
            send_email(sub,des,str(self.request.user.email))
        context = {'form':form}
        return redirect('sellers:AddItem')

class ItemDetailView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        item=SellerItem.objects.get(slug=kwargs['slug'],owner=self.request.user)
        form = ItemForm(initial={'category':str(item.category),'description':str(item.description)})
        context = {'item':item}
        return render(self.request,'sitemdetail.html',context=context)
    def post(self,*args,**kwargs):
        form = ItemForm(self.request.POST or None)
        if form.is_valid() or True:
            item=SellerItem.objects.get(slug=kwargs['slug'],owner=self.request.user)
            item.title=form.cleaned_data.get('title')
            item.price=form.cleaned_data.get('price')            
            item.description=form.cleaned_data.get('description')
            if self.request.FILES.get('img'):
                item.image=self.request.FILES.get('img')
            if self.request.POST.get('sizecheck'):
                item.has_size=True
                item.size=self.request.POST.get('size')            
            item.pweight=self.request.POST.get('weight')
            item.save()            
            images = self.request.FILES.getlist("imgs")
            i=0                        
            for image in images:                
                name = 'rp'+str(i)+str(self.request.user.username)+str(item.title)[:6]
                i+=1
                rimg = Multiple_Pics.objects.create(image=image, name=name)
                item.pis.add(rimg)
            item.save()   
            sub="Review A New Product - From "+str(self.request.user.username)
            des = 'Mr./Mrs. '+str(self.request.user.username)+' has changed a exsisting product in your store, Please review it.'
            send_email(sub,des,str(self.request.user.email))
        context = {'form':form}
        return redirect('sellers:AddItem')

@login_required
def itemimgrem(request, slug, id):
    item=get_object_or_404(SellerItem,slug=slug,owner=request.user)
    img=get_object_or_404(Multiple_Pics,id=id)
    item.pis.remove(img)      
    return HttpResponse("done")

class SellerView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        items = SellerItem.objects.filter(owner=self.request.user)
        context={'object_list':items}
        return render(self.request,'seller.html',context)
    def post(self,*args,**kwargs):
        pass