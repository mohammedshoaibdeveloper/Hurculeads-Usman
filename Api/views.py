from telnetlib import ENCRYPT
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
import Api.usable as uc
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
import jwt 
import datetime
from decouple import config
# Create your views here.
# Create your views here.

# ADMIN AND COMPANY SIGNUP API
class Signup(APIView):
    def post(self, request):
        requireFields = ['firstname','lastname','email','password','phone','address','city','country','username','zipcode','role','verticalid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            phone = request.data.get('phone')
            address = request.data.get('address')
            city = request.data.get('city')
            country = request.data.get('country')
            username = request.data.get('username')
            zipcode = request.data.get('zipcode')
            role = request.data.get('role')
            verticalid = request.data.get('verticalid')
            

            getverticalobj = vertical.objects.filter(id = verticalid).first()
            
            if uc.checkemailforamt(email):
                        if not uc.passwordLengthValidator(password):
                            
                            return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"})
        
                        checkemail = account.objects.filter(email = email).first()
                        if checkemail:
                            return Response({"status":False,"message":"Email alreay exist"},409)
                
                        checkphone = account.objects.filter(phone = phone).first()
                        if checkphone:
                            return Response({"status":False,"message":"Phone number already registered please enter different number"},409)

                        data = account(firstname=firstname,lastname=lastname,email=email,password=handler.hash(password),phone=phone,address=address,city=city,country=country,username=username,zipcode=zipcode,role = role,verticalid=getverticalobj)
                        data.save()

                        return Response({"status":True,"message":"Account Created Successfully"},201)
    
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"},422)

#==================================================================================================================
# ADMIN AND COMPANY LOGIN API

class login(APIView):
    def post(self, request):
        requireFields = ['email','password']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            email = request.data.get('email')
            password = request.data.get('password')

            fetchAccount = account.objects.filter(email=email).first()
            if fetchAccount:
                if handler.verify(password,fetchAccount.password):
                    if fetchAccount.role == "admin":
                        access_token_payload = {
                                        'id': fetchAccount.id,
                                        'name':fetchAccount.firstname, 
                                        'email':fetchAccount.email, 
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                        'iat': datetime.datetime.utcnow(),

                                }

                        access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                        data = {'id':fetchAccount.id,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'address':fetchAccount.address,'email':fetchAccount.email,'phone':fetchAccount.phone,'city':fetchAccount.city,'country':fetchAccount.country,'username':fetchAccount.username,'zipcode':fetchAccount.zipcode,'role':fetchAccount.role }
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data},200)

                    # COMPANY LOGIN API
                    else: 
                        access_token_payload = {
                                    'id': fetchAccount.id,
                                    'name':fetchAccount.firstname, 
                                    'email':fetchAccount.email, 
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                                    'iat': datetime.datetime.utcnow(),

                            }

                        access_token = jwt.encode(access_token_payload,config('companykey'),algorithm = 'HS256')
                        data = {'id':fetchAccount.id,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'address':fetchAccount.address,'email':fetchAccount.email,'phone':fetchAccount.phone,'city':fetchAccount.city,'country':fetchAccount.country,'username':fetchAccount.username,'zipcode':fetchAccount.zipcode,'role':fetchAccount.role }
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"companydata":data},200)

                else:
                    return Response({"status":False,"message":"Invalid crediatials"},200)

            else:
                return Response({"status":False,"message":"Account doesnot access"})

#==================================================================================================================
# VERTICAL ADD,UPDATE,DELETE,GET
# POST API

class verticals(APIView):
    def post(self, request):
        requireFields = ['name']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            name = request.data.get('name')

            data = vertical(name=name)
            data.save()

            return Response({"status":True,"message":"Vertical Created Successfully"})

#############################################################################################################
# GET API

    def get(self, request):
        data = vertical.objects.all().values('id','name').order_by('-id')
        return Response({"status":True,"data":data})

#############################################################################################################
# PUT API

    def put (self, request):
        requireFields = ['id','name']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.data.get("id")
            name = request.data.get("name")
            
            checkvertical = vertical.objects.filter(id = id).first()
            if checkvertical:
                checkvertical.name = name 

                checkvertical.save()

                return Response({"status":True,"message":"Vertical Updated Successfully"})
            else:
                return Response({"status":True,"message":"Data not found"})

#############################################################################################################
# DELETE API

    def delete(self,request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.GET['id']
            data = vertical.objects.filter(id=id).first()
            if data:
                data.delete()
                return Response({"status":True,"message":"Data Deleted Successfully"})
            else:
                return Response({"status":False,"message":"Data not Found"})
    
#############################################################################################################
# Getspecific API

class Getspecificvertical(APIView):
    def get (self, request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.GET['id']
            data = vertical.objects.filter(id = id).values("id","name").first()
            if data:
                return Response({"status":True,"data":data},200)
            else:
                return Response({"status":False,"message":"Data not found"})

# ================================================================================================================
# EMPLOYEE ADD,UPDATE,DELETE,GET
# POST API

class Employee(APIView):
    def post (self, request):
        requireFields = ['firstname','lastname','email','password','phone','address','city','country','username','accountid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            phone = request.data.get('phone')
            address = request.data.get('address')
            city = request.data.get('city')
            country = request.data.get('country')
            username = request.data.get('username')
            accountid = request.data.get('accountid')

            getaccountobj = account.objects.filter(id = accountid).first()

            if uc.checkemailforamt(email):
                if not uc.passwordLengthValidator(password):
                    
                    return Response({"status":False,"message":"Password should not be less than 8 or greater than 20"})

                checkemail = employee.objects.filter(email = email).first()
                if checkemail:
                    return Response({"status":False,"message":"Email alreay exist"},409)
        
                checkphone = employee.objects.filter(phone = phone).first()
                if checkphone:
                    return Response({"status":False,"message":"Phone number already registered please enter different number"},409)

                data = employee(firstname = firstname, lastname = lastname, email = email,password = handler.hash(password), phone = phone, address = address,city = city,country = country,username = username,accountid = getaccountobj)
                data.save()

                return Response({"status":True,"message":"Employee Account has been created"},200)
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"},422)                    

#############################################################################################################
# GET API

    def get (self, request):
       
            data = employee.objects.all().values('id','firstname','lastname','email','password','phone','address','city','country','username','accountid').order_by('-id')
            return Response({"status":True,"data":data})

#############################################################################################################
# PUT API

    def put(self, request):
        requireFields = ['id','firstname','lastname','email','password','phone','address','city','country','username','accountid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.data.get("id")
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            phone = request.data.get('phone')
            city = request.data.get('city')
            country = request.data.get('country')
            username = request.data.get('username')
            accountid = request.data.get('accountid')
            address = request.data.get('address')

            getaccountobj = account.objects.filter(id = accountid).first()
            checkemployee = employee.objects.filter(id = id).first()
            if checkemployee:
                checkemployee.firstname =firstname
                checkemployee.lastname =lastname
                checkemployee.email =email
                checkemployee.password =password
                checkemployee.phone =phone
                checkemployee.city =city
                checkemployee.country =country
                checkemployee.username =username
                checkemployee.accountid =getaccountobj
                checkemployee.address =address

                checkemployee.save()
                
                return Response({"status":True,"message":"Employee data Successfully Updated"})

#############################################################################################################
# DELETE API

    def delete(self, request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.GET['id']
            data = employee.objects.filter(id=id).first()
            if data:
                data.delete()
                return Response({"status":True,"message":"Data Deleted Successfully"})
            else:
                return Response({"status":False,"message":"Data not Found"})

#############################################################################################################
# Getspecific API

class Getspecificemployeedata(APIView):
    def get(self, request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.GET['id']
            data = employee.objects.filter(id = id).values('id','firstname','lastname','email','password','phone','address','city','country','username','accountid').first()
            if data:
                return Response({"status":True,"data":data},200)
            else:
                return Response({"status":False,"message":"Data not found"})

#==================================================================================================================
# VENDOR ADD,UPDATE,DELETE,GET
# POST API

class vendors(APIView):
    def post(self, request):
        requireFields = ['vendorname','created_at','priceperlead','createdby','verticalid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            vendorname = request.data.get('vendorname')
            verticalid = request.data.get('verticalid')
            created_at = request.data.get('created_at')
            priceperlead = request.data.get('priceperlead')
            createdby = request.data.get('createdby')

            getvendorobj = vertical.objects.filter(id = verticalid).first()


            data = vendor(vendorname =vendorname,created_at =created_at,priceperlead =priceperlead,createdby =createdby,verticalid =getvendorobj)
            data.save()

            return Response({'status':True,'message':'Vendor add successfully'})
        
#############################################################################################################
# GET API

    def get (self, request):
        data = vendor.objects.all().values('id','vendorname','verticalid','created_at','priceperlead','createdby').order_by('-id')
        return Response({"status":True,"data":data})

#############################################################################################################
# PUT API

    def put (self, request):
        requireFields = ['id','vendorname','created_at','priceperlead','createdby','verticalid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.data.get('id')
            vendorname = request.data.get('vendorname')
            verticalid = request.data.get('verticalid')
            created_at = request.data.get('created_at')
            priceperlead = request.data.get('priceperlead')
            createdby = request.data.get('createdby')
            getvendorobj = vertical.objects.filter(id = verticalid).first()

            checkvendor = vendor.objects.filter(id = id).first()
            if checkvendor:
                checkvendor.vendorname = vendorname
                checkvendor.verticalid = getvendorobj
                checkvendor.created_at = created_at
                checkvendor.priceperlead = priceperlead
                checkvendor.createdby = createdby

                checkvendor.save()

                return Response({"status":True,"message":"Vendor Updated Successfully"})
            else:
                return Response({"status":False,"message":"Vendor not found"})

#############################################################################################################
# DELETE API

    def delete (self, request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            id = request.GET['id']
            data = vendor.objects.filter(id=id).first()
            if data:
                data.delete()
                return Response({"status":True,"message":"Data Deleted Successfully"})
            else:
                return Response({"status":False,"message":"Data not Found"})

#############################################################################################################
# GETSPECIFICVENDOR API

class GetSpecificvendor(APIView):
    def get(self, request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = vendor.objects.filter(id = id).values('id','vendorname','verticalid','created_at','priceperlead','createdby').first()
                if data:
                    return Response({"status":True,"data":data})
                else:
                    return Response({"status":True,"message":"Data not found"})
                
#==================================================================================================================
# COMPANYLIST ADD,UPDATE,DELETE,GET

class companylists(APIView):
    def post(self, request):
        requireFields = ['companyid','verticalid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                companyid = request.data.get('companyid')
                verticalid = request.data.get('verticalid')

                getcompanyobj = account.objects.filter(id = companyid).first()
                getverticalobj = vertical.objects.filter(id = verticalid).first()

                data = companylist(companyid = getcompanyobj,verticalid = getverticalobj)
                data.save()

                return Response({'status':True,'message':'Successfully created company list'})
 
#############################################################################################################
# GET API
   
    def get(self,request):
        my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
        if my_token:
             data = companylist.objects.all().values('id','companyid','verticalid').order_by('-id')
             return Response({"status":True,"data":data})

#############################################################################################################
# PUT API
   
    def put(self, request):
        requireFields = ['id','companyid','verticalid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.data.get('id')
                companyid = request.data.get('companyid')
                verticalid = request.data.get('verticalid')

                getcompanyobj = account.objects.filter(id = companyid).first()
                getverticalobj = vertical.objects.filter(id = verticalid).first()

                checkcompanylist = companylist.objects.filter(id = id).first()
                if checkcompanylist:
                    checkcompanylist.companyid = getcompanyobj
                    checkcompanylist.verticalid = getverticalobj

                    checkcompanylist.save()

                    return Response({'status':True,'message':'Successfully updated company list'})

#############################################################################################################
# DELETE API

    def delete(self, request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = companylist.objects.filter(id=id).first()
                if data:
                    data.delete()
                    return Response({"status":True,"message":"Data Deleted Successfully"})
                else:
                    return Response({"status":False,"message":"Data not Found"})

#############################################################################################################
# GETSPECIFIC COMPANYLIST API
class getspecificcomanylist(APIView):
    def get(self, request):
        requireFields = ['id']
        validator = uc.keyValidation(True,True,request.GET,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            my_token = uc.tokenauth(request.META['HTTP_AUTHORIZATION'][7:])
            if my_token:
                id = request.GET['id']
                data = companylist.objects.filter(id = id).values('id','id','companyid','verticalid').first()
                if data:
                    return Response({"status":True,"data":data})
                else:
                    return Response({"status":True,"message":"Data not found"})

#==================================================================================================================
# CUSTUMER SIGN IN

class customersignin(APIView):
    def post(self, request):
        requireFields = ['firstname', 'lastname', 'email','password','phone','state','city','country','username','zipcode']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator,status = 200)
        
        else:
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            phone = request.data.get('phone')
            state = request.data.get('state')
            city = request.data.get('city')
            country = request.data.get('country')
            username = request.data.get('username')
            zipcode = request.data.get('zipcode')

            if uc.checkemailforamt(email):
                if not uc.passwordLengthValidator(password):
                            
                    return Response({"status":False,"message":"Password should not be less than 8 or greater than 20!"})
        
                checkemail = customer.objects.filter(email = email).first()
                if checkemail:

                    return Response({"status":False,"message":"Email alreay exist!"},409)
                
                checkphone = customer.objects.filter(phone = phone).first()
                if checkphone:

                    return Response({"status":False,"message":"Phone number already exist please try enter different number!"},409)

                data = customer(firstname=firstname,lastname=lastname,email=email,password=handler.hash(password),phone=phone,state=state,city=city,country=country,username=username,zipcode=zipcode)
                data.save()

                return Response({"status":True,"message":"Custumer Successfully Signin"},201)
    
            else:
                return Response({"status":False,"message":"Email Format Is Incorrect"},422)