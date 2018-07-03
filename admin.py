from django.contrib import admin

# Register your models here.
from .models import Item,Company,Sales,Inventory,Store,Customer,Employee,Account,Expense


admin.site.register(Item)
admin.site.register(Company)
admin.site.register(Sales)
admin.site.register(Inventory)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Store)
admin.site.register(Account)
admin.site.register(Expense)