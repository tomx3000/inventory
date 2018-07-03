from rest_framework import serializers

from .models import Sales,Store,Employee,Company,Customer,Inventory,Item,Account,Expense
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model =User
		fields ="__all__"

class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model =Account
		fields ="__all__"

class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model =Expense
		fields ="__all__"

class SalesSerializer(serializers.ModelSerializer):
	class Meta:
		model =Sales
		fields ="__all__"

class StoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Store
		fields= "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields="__all__"

class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model= Company
		fields="__all__"

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model=Customer
		fields="__all__"

class InventorySerializer(serializers.ModelSerializer):
	class Meta:
		model=Inventory
		fields="__all__"

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model= Item
		fields="__all__"






