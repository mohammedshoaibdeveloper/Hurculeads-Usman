from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(vertical)
admin.site.register(account)
admin.site.register(employee)
admin.site.register(vendor)
admin.site.register(companylist)
admin.site.register(customer)


admin.site.site_header = 'HURCULEAD'
