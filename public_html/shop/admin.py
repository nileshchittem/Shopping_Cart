from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.
class itemAdmin(admin.ModelAdmin):
	list_display = ('item_name','item_quantity','item_cost','item_discount','item_seller')
	list_filter = ['item_seller']
	search_fields = ['item_name','item_quantity','item_cost','item_discount','item_description','item_seller']

class transactionAdmin(admin.ModelAdmin):
	list_display = ('id','t_date','t_cost')
	list_filter = ['t_date']
	search_fields = ['id','t_date','t_cost']

'''class customerAdmin(admin.ModelAdmin):
	list_display = ('user.username','user.password','user.email')
	#list_filter = ['id']
	search_fields = ['user.username','user.email']'''

admin.site.register(item,itemAdmin)
admin.site.register(transaction,transactionAdmin)
admin.site.register(cart)
admin.site.register(customer)
admin.site.register(seller)
admin.site.register(order)
