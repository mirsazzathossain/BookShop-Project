from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from .models import *
from django import template
from django.http.response import HttpResponse, JsonResponse
import collections
from django.db.models import F

# Create your views here.

def store(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'shop/home.html', context)

def cart(request):
    user = request.user
    if request.method == 'POST':
        productId = request.POST.getlist('productId')
        qty = request.POST.getlist('quantity')
        if request.user.is_anonymous:
            for product, quantity in zip(productId, qty):
                cartItem={}
                cartItem[product] = {
                    'quantity': int(quantity)
                }
                if 'cartdata' in request.session:
                    if str(product) in request.session['cartdata']:
                        cart_data=request.session['cartdata']
                        cart_data[str(product)]['quantity'] = int(quantity)
                        cart_data.update(cart_data)
                        request.session['cartdata']=cart_data   
                if request.session['cartdata'][str(product)]['quantity'] <= 0:
                    request.session['cartdata'].pop(str(product))
        else:
            for product, quantity in zip(productId, qty):
                book = Book.objects.get(id=int(product))
                cart, created = Cart.objects.get_or_create(user=user)

                cartItem, created = CartItem.objects.get_or_create(cart=cart, product=book)

                cartItem.quantity = int(quantity)
                cartItem.save()

                if cartItem.quantity <= 0:
                    cartItem.delete()

    if request.user.is_anonymous:
        cart =[]
        if 'cartdata' in request.session:
            for key in request.session['cartdata']:
                cart_data=request.session['cartdata']
                quantity = cart_data[key]['quantity']
                book = Book.objects.get(id=int(key))
                dictionary = {"quantity":quantity, "product": book}
                cartItem = collections.namedtuple("CartItem", dictionary.keys())(*dictionary.values())
                cart.append(cartItem)

        return render(request, 'shop/cart.html', {'cart': cart})

    else:
        cart = Cart.objects.get(user=user)
        items = CartItem.objects.filter(cart=cart)

        return render(request, 'shop/cart.html', {'cart': items})

def checkout(request):
    user = request.user

    if request.method == 'POST':
        print(request.POST)
        name = request.POST['billing_first_name']+' '+request.POST['billing_first_name']
        address = request.POST['billing_address_1']+', '+request.POST['billing_address_2']+', '+request.POST['billing_city']+', '+request.POST['billing_postcode']+', ' + request.POST['billing_country']
        phone = request.POST['billing_phone']
        email = request.POST['billing_email']
        notes = request.POST['order_comments']
        total = 0

        if request.user.is_anonymous:
            if 'cartdata' in request.session:
                for key in request.session['cartdata']:
                    cart_data=request.session['cartdata']
                    quantity = cart_data[key]['quantity']
                    book = Book.objects.get(id=int(key))
                    total += book.price * quantity
            
            del request.session['cartdata']
        else:
            cart = Cart.objects.get(user=user)
            items = CartItem.objects.filter(cart=cart)
            for item in items:
                total += item.quantity * item.product.price

            items.delete()
        
        order = Order(name=name, address=address, phone=phone, email=email, notes=notes, amount=total)
        order.save()
        
        return redirect('/')


    if request.user.is_anonymous:
        cart =[]
        if 'cartdata' in request.session:
            for key in request.session['cartdata']:
                cart_data=request.session['cartdata']
                quantity = cart_data[key]['quantity']
                book = Book.objects.get(id=int(key))
                dictionary = {"quantity":quantity, "product": book}
                cartItem = collections.namedtuple("CartItem", dictionary.keys())(*dictionary.values())
                cart.append(cartItem)

        return render(request, 'shop/checkout.html', {'cart': cart})

    else:
        cart = Cart.objects.get(user=user)
        items = CartItem.objects.filter(cart=cart)
        return render(request, 'shop/checkout.html', {'cart': items})

def details(request, id):
    user = request.user
    total = 1

    if request.method == 'POST':
        productId = request.POST['productId']
        qty = request.POST['quantity']

        if request.user.is_anonymous:
            cartItem={}
            cartItem[str(productId)] = {
                'quantity': int(qty)
            }
            if 'cartdata' in request.session:
                if str(productId) in request.session['cartdata']:
                    cart_data=request.session['cartdata']
                    cart_data[str(productId)]['quantity'] = int(qty)
                    cart_data.update(cart_data)
                    request.session['cartdata']=cart_data
                else:
                    cart_data=request.session['cartdata']
                    cart_data.update(cartItem)
                    request.session['cartdata']=cart_data
            else:
                request.session['cartdata']=cartItem     
        else:
            book = Book.objects.get(id=productId)
            cart, created = Cart.objects.get_or_create(user=user)

            cartItem, created = CartItem.objects.get_or_create(cart=cart, product=book)

            cartItem.quantity = int(qty)
            cartItem.save()

    if request.user.is_anonymous:
        if 'cartdata' in request.session:
            if str(id) in request.session['cartdata']:
                total = int(request.session['cartdata'][str(id)]['quantity'])
    else:
        cart = Cart.objects.get(user=user)
        items = CartItem.objects.filter(cart=cart)
        for item in items:
            if item.product.id == id:
                total = item.quantity

    books = Book.objects.all()
    book = Book.objects.get(id=id)

    context = {'book': book, 'books': books, 'total': total}

    return render(request, 'shop/details.html', context)

def updateItem(request):
    user = request.user
    if request.method == 'POST':
        productId = request.POST['productId']
        qty = request.POST['quantity']
        action = request.POST['action']
        

        if request.user.is_anonymous:
            cartItem={}
            cartItem[str(productId)] = {
                'quantity': int(qty)
            }
            if action == 'add':
                if 'cartdata' in request.session:
                    if str(productId) in request.session['cartdata']:
                        cart_data=request.session['cartdata']
                        cart_data[str(productId)]['quantity'] += int(qty)
                        cart_data.update(cart_data)
                        request.session['cartdata']=cart_data
                    else:
                        cart_data=request.session['cartdata']
                        cart_data.update(cartItem)
                        request.session['cartdata']=cart_data
                else:
                    request.session['cartdata']=cartItem     
            elif action == 'remove':
                if 'cartdata' in request.session:
                    if str(productId) in request.session['cartdata']:
                        cart_data=request.session['cartdata']
                        cart_data[str(productId)]['quantity'] -= int(qty)
                        cart_data.update(cart_data)
                        request.session['cartdata']=cart_data
                    
                        if request.session['cartdata'][str(productId)]['quantity'] <= 0:
                            request.session['cartdata'].pop(str(productId))
            elif action == 'delete':
                if 'cartdata' in request.session:
                    request.session['cartdata'].pop(str(productId))
        else:
            book = Book.objects.get(id=productId)
            cart, created = Cart.objects.get_or_create(user=user)

            cartItem, created = CartItem.objects.get_or_create(cart=cart, product=book)

            if action == 'add':
                cartItem.quantity = (cartItem.quantity+int(qty))
                cartItem.save()
            elif action == 'remove':
                cartItem.quantity = (cartItem.quantity-int(qty))
                cartItem.save()
            elif action == 'delete':
                cartItem.delete()


            if cartItem.quantity <= 0:
                cartItem.delete()
    
    if request.user.is_anonymous:
        total = 0

        if 'cartdata' in request.session:
            for key in request.session['cartdata']:
                cart_data=request.session['cartdata']
                total += cart_data[key]['quantity']
        return JsonResponse({'total': total})
    else:
        total = 0
        
        if Cart.objects.get(user=user):
            cart = Cart.objects.get(user=user)
            if CartItem.objects.filter(cart=cart).exists():
                cart = Cart.objects.get(user=user)
                items = CartItem.objects.filter(cart=cart)

                for item in items:
                    total = total + item.quantity

        return JsonResponse({'total': total})


def shop(request):
    if not request.GET:
        books = Book.objects.all()
    elif request.GET['orderby'] == 'date':
        books = Book.objects.all()
    elif request.GET['orderby'] == 'price':
        books = Book.objects.all().order_by('price')
    elif request.GET['orderby'] == 'price-desc':
        books = Book.objects.all().order_by(F('price').desc())
    return render(request, 'shop/shop.html', {'books': books})