from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from .models import Message, Product
from .forms import ProductForm


# Create your views here.



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    return render(request, 'base/login_register.html', {'page': 'login'})


def registerPage(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'base/login_register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
    context = {'products': products}
    return render(request, 'base/home.html', context)


def userProfile(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {'user': user}
    return render(request, 'base/user_profile.html', context)


def product_list(request):
    product = Product.objects.all()
    return render(request, 'base/product_list.html', {'product': product})


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'base/product_details.html', {'product': product})


def sell_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'base/sell_products.html', {'form': form})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed to delete this product')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj' : message})

@login_required(login_url='login')
def createProducts(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid(): 
            Products = form.save(commit=False)
            Products.owner = request.user
            Products.save()
            return redirect('home')
        
    context = {'form' : form}
    return render(request, 'base/products_form.html', context)

@login_required(login_url='login')
def updateProducts(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = ProductForm(instance=product)

    if request.user != product.owner:
        return HttpResponse('You are not allowed to update this product')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/products_form.html', context)

@login_required(login_url='login')
def deleteProducts(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.user != product.owner:
        return HttpResponse('You are not allowed to delete this product')
    
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': product})

def Shop(request, shop_id):
    # Get the shop object
    shop = get_object_or_404(Shop, id=shop_id)
    
    # Check if the logged-in user is the owner of the shop
    if request.user != shop.owner:
        return redirect('home')  # Or any other page or action
    
    # Get products associated with the shop
    products = Product.objects.filter(shop=shop)
    
    # Pass shop and products to the template
    return render(request, 'shop.html', {'shop': shop, 'products': products})

def add_product_to_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    
    # Ensure that the logged-in user is the owner of the shop
    if request.user != shop.owner:
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            shop.products.add(product)
            return redirect('shop_detail', shop_id=shop_id)
    else:
        form = ProductForm()
    
    return render(request, 'add_product_to_shop.html', {'form': form})