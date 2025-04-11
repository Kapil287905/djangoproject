from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# userdetail
# products
# ccarts
# orders
# orderstatus
# payments
class UserDetail(models.Model):
    userid = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=None)
    type = (("Male","Male"),("Female","Fmeale"))
    gender = models.CharField(max_length=30,choices=type)
    dob = models.DateField(null=True,default=None)
    mobile = models.PositiveIntegerField()
    address = models.TextField()
    photo = models.ImageField(upload_to="images")

class Products(models.Model):
    userid = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=None)
    product_id = models.PositiveIntegerField(primary_key=True)
    product_name = models.CharField(max_length=100)
    type=(("Mobile","Mobile"),("Cloths","Cloths"),("Shoses","Shoses"),("Electronics","Electronics"))
    category = models.CharField(max_length=30,choices=type)
    description = models.TextField()
    price =models.FloatField()
    image = models.ImageField(upload_to="images")

class Carts(models.Model):
    userid = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=None)
    productid = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True,default=None)
    quantity = models.PositiveIntegerField(default=0)
       
class Orders(models.Model):
    orderid = models.PositiveIntegerField(primary_key=True)
    userid = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=None)
    productid = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True,default=None)
    quantity = models.PositiveIntegerField(default=0)
    orderdate = models.DateField()

class Payments(models.Model):
    receiptid = models.PositiveIntegerField(primary_key=True)
    orderid = models.ForeignKey(Orders,on_delete=models.SET_NULL,null=True,default=None)
    userid = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=None)    
    productid = models.ForeignKey(Products,on_delete=models.SET_NULL,null=True,default=None)
    ptype=(("Online","Online"),("Cash on delivery","Cash on delivery"))
    paymenttype = models.CharField(max_length=30,choices=ptype)
    type = (("Done","Done"),("Failed","Failed"))
    paymentstatus = models.CharField(max_length=30,choices=type)

    
