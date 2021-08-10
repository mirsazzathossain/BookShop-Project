from django.shortcuts import render
from .models import *
from django import template

# Create your views here.

def store(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'shop/store.html', context)

def cart(request):
    context = {}
    return render(request, 'shop/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'shop/checkout.html', context)

