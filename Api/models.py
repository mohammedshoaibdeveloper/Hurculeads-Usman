from django.db import models
from django import forms

# Create your models here.
roles = (
    ("admin", "admin"),
    ("company","company"),
)
class vertical(models.Model):
    name = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.name

class account(models.Model):
    firstname = models.CharField(max_length=255,default='')
    lastname = models.CharField(max_length=255,default='')
    email = models.EmailField(max_length=255,default='')
    password = models.CharField(max_length=255,default='')
    phone = models.CharField(max_length=255,default='',unique=True)
    address = models.CharField(max_length=255,default='')
    city = models.CharField(max_length=255,default='')
    country = models.CharField(max_length=255,default='')
    username = models.CharField(max_length=255,default='')
    zipcode = models.CharField(max_length=255,default='')
    role = models.CharField(choices=roles,max_length=20,default="admin")
    verticalid = models.ForeignKey(vertical,on_delete=models.CASCADE,blank=True,null=True) # fr
    
    def __str__(self):
        return self.firstname

class employee(models.Model):
    firstname = models.CharField(max_length=255,default= '')
    lastname = models.CharField(max_length=255,default= '')
    email = models.EmailField(max_length=255,default= '')
    password = models.CharField(max_length=255,default= '')
    phone = models.CharField(max_length=255,default= '',unique=True)
    address = models.CharField(max_length=255,default= '')
    city = models.CharField(max_length=255,default= '')
    country = models.CharField(max_length=255,default= '')
    username = models.CharField(max_length=255,default= '')
    accountid = models.ForeignKey(account,on_delete=models.CASCADE,blank=True,null=True) # fr

    def __str__(self):
        return self.firstname

class vendor(models.Model): 
    vendorname = models.CharField(max_length=255,default='')
    verticalid = models.ForeignKey(vertical,on_delete=models.CASCADE,blank=True,null=True) # fr
    created_at = models.DateField(null=False)
    priceperlead = models.FloatField(null=True, blank=True, default=0)
    createdby= models.CharField(choices=roles,max_length=20,default="admin")

    def __str__(self):
        return self.vendorname

class companylist(models.Model):
    companyid = models.ForeignKey(account,on_delete=models.CASCADE,blank=True,null=True) # fr
    verticalid = models.ForeignKey(vertical,on_delete=models.CASCADE,blank=True,null=True) # fr

class customer(models.Model):
    firstname = models.CharField(max_length=255,default= '')
    lastname = models.CharField(max_length=255,default= '')
    email = models.CharField(max_length=255,default= '')
    phone = models.CharField(max_length=255,default= '',unique=True)
    city = models.CharField(max_length=255,default= '')
    state = models.CharField(max_length=255,default= '')
    zipcode = models.CharField(max_length=255,default= '')
    country = models.CharField(max_length=255,default= '')
    username = models.CharField(max_length=255,default= '')
    password = models.CharField(max_length=255,default= '')
    
    def __str__(self):
        return self.firstname

