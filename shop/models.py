from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    description   = models.TextField(null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=200, null=True)
    ISBN = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    authors = models.ManyToManyField(Author)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.id

class CartItem(models.Model):
    product = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return (self.product.name)

class Order(models.Model):
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=400, null=True)
    phone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=True)
    notes = models.CharField(max_length=400, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=False)