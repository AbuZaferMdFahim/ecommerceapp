from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render,HttpResponse
from django.http import JsonResponse

from django.shortcuts import render

from django.views import View
from django.contrib import messages
from app.forms import CustomRegistrationForm,CustomerProfileForm
from .models import Cart, Product,Customer
from django.db.models import Q
# Create your views here.

def home(request):
    return render(request,"app/home.html")
def about(request):
    return render(request,"app/about.html")
def contact(request):
    return render(request,"app/contact.html")

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

def addtoCart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def showCart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity* p.product.discounted_price
        amount = amount+value
    totalamount = amount+40 
    return render(request, 'app/addtoCart.html',locals())

def plusCurt(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q (user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user) 
        for p in cart:
            value = p.quantity* p.product.discounted_price
            amount = amount+value
        totalamount = amount+40 
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount

        }
        return JsonResponse(data)


class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class CategoryTitleView(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetailView(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomRegistrationForm()    
        return render(request,'app/CustomerRegistration.html',locals())
    def post(self,request):
        form = CustomRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Congratulation! User is Registered Succesfully')
        else:
            messages.error(request, 'Invalid Input Data ')
        return render(request,'app/CustomerRegistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
        
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            division = form.cleaned_data['division']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user = user,name=name, locality=locality,city=city,mobile=mobile,division=division,zipcode=zipcode)
            reg.save()

            messages.success(request,'Congratulation! Profile Saved Succesfully')
            
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html',locals())
    
class UpdateAddressView(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.division = form.cleaned_data['division']
            add.zipcode = form.cleaned_data['zipcode'] 
            add.save()
            messages.success(request,'Congratulation! Profile Updated Succesfully')
        else:
            messages.warning(request, "Invalid Input Data")
