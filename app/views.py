
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from app.forms import CustomRegistrationForm,CustomerProfileForm,ProductForm
from app.serializers import ProductSerializer
from .models import Cart, Product,Customer,Wishlist
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from django.contrib import messages

def home(request):
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    messages_info = messages.get_messages(request)

    return render(request, "app/home.html", {'totalitem': totalitem, 'wishitem': wishitem, 'messages_info': messages_info})

def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())
def contact(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

@login_required
def address(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())

@login_required
def addProduct(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            # Add any additional logic or redirect as needed
    else:
        form = ProductForm()

    return render(request, 'app/addProduct.html', locals())

@login_required
def addtoCart(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def showCart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity* p.product.discounted_price
        amount = amount+value
    totalamount = amount+40 
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtoCart.html',locals())

@login_required
def plusCurt(request):
    if request.method =='GET':
        try:
            prod_id = request.GET['prod_id']
            user = request.user
            carts = Cart.objects.filter(product=prod_id, user=user)
                
           
            if carts.exists():
                
                cart_item = carts.first()
                cart_item.quantity += 1
                cart_item.save()
                    
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40
                    
                data = {
                    'quantity': cart_item.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                    }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)
            
        except MultipleObjectsReturned:
            
            return JsonResponse({'error': 'Multiple Cart items found'}, status=500)
        except Exception as e:
            
            print("Error:", str(e))
            return JsonResponse({'error': 'An error occurred'}, status=500)

@login_required
def minusCurt(request):
    if request.method =='GET':
        try:
            prod_id = request.GET['prod_id']
            user = request.user
            carts = Cart.objects.filter(product=prod_id, user=user)
                
            
            if carts.exists():
               
                cart_item = carts.first()
                cart_item.quantity -= 1
                cart_item.save()
                    
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40
                    
                data = {
                    'quantity': cart_item.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                    }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)
            
        except MultipleObjectsReturned:
          
            return JsonResponse({'error': 'Multiple Cart items found'}, status=500)
        except Exception as e:
           
            print("Error:", str(e))
            return JsonResponse({'error': 'An error occurred'}, status=500)

@login_required        
def removeCurt(request):
    if request.method == 'GET':
        try:
            prod_id = request.GET['prod_id']
            

            c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
            
            if c:
                c.delete()
                
                user = request.user
                cart = Cart.objects.filter(user=user) 
                amount = 0
                for p in cart: 
                    value = p.quantity * p.product.discounted_price
                    amount += value
                totalamount = amount + 40 
                
                data = {
                    'amount': amount,
                    'totalamount': totalamount
                }
                
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item not found'}, status=404)
        except Exception as e:
            # Print or log the error message for debugging
            print("Error:", str(e))
            return JsonResponse({'error': 'An error occurred'}, status=500)

@login_required
def plus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'messeages': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'messeages': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)   
    
from django.shortcuts import render, redirect
from django.contrib import messages


def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query)) 
    return render(request,'app/Search.html',locals())



@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')    
class CategoryTitleView(View):
    def get(self,request,val):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        seller = product.seller

        if request.user == seller:
            messages.warning(request, "You cannot order of your own product.")
            return redirect('home') 

        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

        return render(request, 'app/productdetail.html', {'product': product, 'totalitem': totalitem, 'wishitem': wishitem})




   
class CustomerRegistrationView(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
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

@method_decorator(login_required,name='dispatch')    
class ProfileView(View):
    def get(self,request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
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
    
@method_decorator(login_required,name='dispatch')    
class UpdateAddressView(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
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

@method_decorator(login_required,name='dispatch')
class checkoutView(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount+value
        totalamount = famount+40 
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/checkout.html',locals())
    

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            


