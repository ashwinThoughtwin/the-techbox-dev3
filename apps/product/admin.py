from django.contrib import admin
from .models import Employee,Item,ItemAssign,SellItems
# Register your models here.
class AdminEmployee(admin.ModelAdmin):
    list_display = ['name','designation','email','mobile']


class AdminItem(admin.ModelAdmin):
    list_display = ['id','name','status']

admin.site.register(Employee,AdminEmployee)
admin.site.register(Item,AdminItem)
admin.site.register(ItemAssign)
admin.site.register(SellItems)