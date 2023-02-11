from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
from . import forms
from django.urls import reverse
from django.contrib.auth.models import auth
from django.contrib.auth import login, authenticate, logout  # add to imports
from cart.cart import Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from qrcode import *
from django.conf import settings
from io import BytesIO
import time
import qrcode

def homePage(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return HttpResponseRedirect(reverse("storeapp:home"))

    else:
        products = None
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        
        if category_id:
            products = Product.objects.filter(category=category_id)
        else:
            products = Product.objects.filter(category=1)
        
        context = {'products': products, 'categories': categories}
        print("Your Username is: ", request.session.get('username'))
        return render(request, 'storeapp/home.html', context)

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            request.session['user'] = username
            return redirect('storeapp:home')
    else:
        form = AuthenticationForm()
    return render(request, 'storeapp/login.html', context={"form":form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('storeapp:home')
    else:
        form = SignUpForm()
    return render(request, 'storeapp/signup.html', {'form': form})   

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("storeapp:login")        


@login_required
def cart(request):
    cart_product_id = (request.session.get('cart').keys())
    cart_product = Product.get_products_by_id(cart_product_id) 
    return render(request, 'storeapp/cart.html', {'cart_product': cart_product})


@login_required
def checkout(request):
    
    if request.method == "POST":
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        user = request.session.get("user")
        cart = request.session.get("cart")
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(user=request.user, product=product, price=product.price, address=address,
                          phone=phone, country=country, state=state, city=city, email=email, zip_code=zip_code, quantity=cart.get(str(product.id)))
            order.save()

        request.session['cart'] = {}

        return redirect("storeapp:cart")
    else:
        cart = request.session.get("cart")
        products = Product.get_products_by_id(list(cart.keys()))
        return render(request, 'storeapp/checkout.html', context={'product':products}) 

@login_required
def orderpage(request):
    
    order = Order.objects.filter(user=request.user)
    print(order)
    return render(request, 'storeapp/order.html', {'order': order})
@login_required
def paystack(request):
    user = request.session.get("user")
    cart = request.session.get("cart")
    products = Product.get_products_by_id(list(cart.keys()))
    return render(request, 'storeapp/paystack.html',context={'product':products})    
@login_required
def order_detaile(request, pk):
    orders = Order.objects.get(id=pk)
    
    return render(request, 'storeapp/order_detaile.html', context={'order':orders,})    

def product_detaile(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product = request.POST.get('product.id')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('storeapp:product_detaile')
    else:
        pass
    product = Product.objects.get(id=pk)
    return render(request, 'storeapp/product_detaile.html', context={'product':product, 'pk':pk})    


def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("storeapp:home")



def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("storeapp:home")



def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("storeapp:home")


def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("storeapp:home")



def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("storeapp:home")


def search_product(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
        
    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.filter(category=1)
    """ search function  """
    if request.method == "POST":
        query_name = request.POST.get('name', None)
        if query_name:
            results = Product.objects.filter(name__contains=query_name)
            return render(request, 'storeapp/search.html', {"results":results})
        
        
               

    return render(request, 'storeapp/search.html', {'categories':categories})


def reviews(request):
    return render(request, 'storeapp/reviews.html')    