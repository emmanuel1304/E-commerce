from enum import unique
from django.db import models
from django.contrib.auth.models import User
import datetime
from django_countries.fields import CountryField
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import random
import string
# Create your models here.

class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=200, blank=False)
    

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(default=0, blank=False)
    old_price = models.IntegerField (default=0, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    description = models.TextField(max_length=500000, blank=False)
    image = models.ImageField(null=True)
    in_stock = models.CharField(max_length=10, blank=False)
    review = models.CharField(max_length=10)


    def __str__(self):
        return self.name

    def get_products_by_id(cart_product_id):
        return Product.objects.filter(id__in=cart_product_id)
    
def generate_random_code():
    characters = '153627363782948473837478754557002124876432345679000987768752287689'
    result=''
    for i in range(0, 14):
        result += random.choice(characters)
    
    return result

def random_string_generator():
    characters = '153627363782948473837478754557002124876432345679000987768752287689'
    result='FF92612'
    for i in range(0, 17):
        result += random.choice(characters)
    
    return result






class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    country = models.CharField(max_length=25, blank=False)
    state = models.CharField(max_length=30, blank=False)
    city = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=11)
    zip_code = models.CharField(max_length=25, blank=False)
    date = models.DateTimeField(default=datetime.datetime.today)
    code = models.CharField(max_length=20, default=generate_random_code, db_index=True)
    status = models.BooleanField(default=False)
    shipping_status = models.BooleanField(default=False)
    shipping_no = models.CharField(max_length=30, default=random_string_generator)
    qr_code = models.ImageField(upload_to='images', blank=True)
    

    
    
    def __str__(self):
        return self.user.username
    
    def get_order_by_customer(user):
        return Order.objects.filter(user=user)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.shipping_no)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.shipping_no}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
