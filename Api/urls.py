from django.urls import path,include
from Api.views import *


urlpatterns = [
#web urls  home
path('',Signup.as_view()),
path('Signup',Signup.as_view()),
path('login',login.as_view()),
path('verticals',verticals.as_view()),
path('Getspecificvertical',Getspecificvertical.as_view()),
path('Employee',Employee.as_view()),
path('Getspecificemployeedata',Getspecificemployeedata.as_view()),
path('vendors',vendors.as_view()),
path('GetSpecificvendor',GetSpecificvendor.as_view()),
path('companylists',companylists.as_view()),
path('getspecificcomanylist',getspecificcomanylist.as_view()),
path('customersignin',customersignin.as_view()),

]