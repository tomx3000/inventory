from django.db import models
from django.conf import settings
from .utility import generate_manufucture
# Create your models here.
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.query import QuerySet



SOMEFIXED = getattr(settings,'FIXE_VALUE',3)

# class SoftDelete(models.Manager):
# 	pass


class SoftDeleteModelQuerySet(QuerySet):
	# this is to handle all delete on a query set , since the baypass a model delete
	def delete(self):
		return super(SoftDeleteModelQuerySet,self).update(deleted_at=timezone.now())
	# this handels hard delete on a query set , not just a model
	def hard_delete(self):
		return super(SoftDeleteModelQuerySet,self).delete()

	def alive(self):
		return self.filter(deleted_at=None)

	def dead(self):
		return self.exclude(deleted_at=None)


class SoftDeleteModelManager(models.Manager):
	def __init__(self,*args,**kargs):
		self.alive_only=kargs.pop('alive_only',True)
		super(SoftDeleteModelManager,self).__init__(*args,**kargs)

	def get_queryset(self):
		if self.alive_only:
			return SoftDeleteModelQuerySet(self.model).filter(deleted_at=None)
		else:
			return SoftDeleteModelQuerySet(self.model)

	def hard_delete(self):
		return self.get_queryset().hard_delete()

	def dead(self):
		return self.get_queryset().dead()




class SoftDeleteModel(models.Model):
	deleted_at=models.DateTimeField(null=True,blank=True)
	objects = SoftDeleteModelManager()
	all_objects=SoftDeleteModelManager(alive_only=False)

	class Meta:
		abstract = True

	def delete(self):
		self.deleted_at=timezone.now()
		self.save()

	def hard_delete(self):
		super(SoftDeleteModel,self).delete()




class ItemManager(models.Manager):
	# overiding the default methods to allow for soft delete and viewing only the undeleted items

	# hope full recovering will be written in bash script, thus bypassing all this django methods 

	# def all(self,*args,**kargs):
	# 	query_set=super(ItemManager,self).all(*args,**kargs)
	# 	# remeber to remove this filter for none , since it is a repetion . this is because filter its self already implements a deleted none filter
	# 	# now = timezone.now()
	# 	qs=query_set.filter(deleted_at=None)

	# 	return qs
	# def filter(self,*args,**kargs):
	# 	now = timezone.now()
	# 	query_set=super(ItemManager,self).filter(*args,**kargs).filter(deleted_at=None)
	# 	qs=query_set

	# 	return qs
	# def get(self,*args,**kargs):
	# 	query_set=super(ItemManager,self).get(*args,**kargs)
	# 	# remeber to remove this filter for none , since it is a repetion . this is because filter its self already implements a deleted none filter
	# 	qs=query_set.filter(deleted_at=None)

	# 	return qs

	# # def update(self,*args,**kargs):
	# # 	query_set=super(ItemManager,self).update(*args,**kargs)
		

	# def delete(self,*args,**kargs):
	# 	now = timezone.now()
	# 	query_set=super(ItemManager,self).update(deleted_at=now)


	# def soft_delete(self,*args,**kargs):
	# 	now = timezone.now()
	# 	query_set=super(ItemManager,self).update(deleted_at=now)
		

	# def hard_delete(self,*args,**kargs):
	# 	query_set=super(ItemManager,self).delete(*args,**kargs)
	# 	pass

	# def is_alive(self,*args,**kargs):
	# 	pass

	# def recover(self,*args,**kargs):
	# 	pass

	# def is_dead(self,*args,**kargs):
	# 	pass


	def check_amount(self,itmes=None):
		qs=Item.objects.filter(id__gte=1)
		amount=0

		# if itmes is not None and isinstance(items,int):
		# 	qs = qs.oder_by('-id')[:items]

		for row in qs:
			amount+=row.item_price
		return "Total :{a}".format(a=amount)	


class Company(SoftDeleteModel):
	company_name=models.CharField(max_length=40,)
	company_address=models.CharField(max_length=40,)
	company_phone=models.CharField(max_length=20,)
	company_email=models.EmailField(max_length=40,)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)
	# instead of calling delete
	# set this field to timezone.now()
	

    

	def __str__(self):
		return str(self.id)+": "+str(self.company_name)
	pass

	def delete(self):
		now = timezone.now()
		query_set=self.update(deleted_at=now)

class Store(SoftDeleteModel):
	company=models.ForeignKey(Company,on_delete=models.CASCADE)
	store_name=models.CharField(max_length=40,)
	store_address=models.CharField(max_length=40,)
	store_phone=models.CharField(max_length=20,)
	store_email=models.EmailField(max_length=40,null=True,blank=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)



	def __str__(self):
		return str(self.store_name)
	pass


class Customer(SoftDeleteModel):
	# adjusting customer name to unique name only
	company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
	customer_name=models.CharField(max_length=40,unique=True)
	customer_transport=models.CharField(max_length=40,null=True,blank=True)
	customer_phone=models.CharField(max_length=20,null=True,blank=True)
	customer_location=models.CharField(max_length=40,null=True,blank=True)
	customer_status=models.BooleanField(default=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)

	# customer amount over paid during loan payment
	# the amount is deducted on next item purchase
	customer_debit_amount=models.FloatField(default=0,null=True,blank=True)


	def __str__(self):
		return str(self.customer_name)

	class Meta:
		ordering=['customer_name']


	pass


class Employee(SoftDeleteModel):
	user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
	company=models.ForeignKey(Company,on_delete=models.CASCADE)
	employee_firstname=models.CharField(max_length=20)
	employee_secondname=models.CharField(max_length=20,null=True,blank=True)
	employee_thirdname=models.CharField(max_length=20,null=True,blank=True)
	employee_phone=models.CharField(max_length=20,null=True,blank=True)
	employee_email=models.EmailField(null=True,blank=True)
	employee_privillage=models.IntegerField(default=1)
	employee_position=models.CharField(max_length=20)
	employee_address=models.CharField(max_length=30,null=True,blank=True)
	employee_sale_limit=models.FloatField(default=50)
	is_active=models.BooleanField(default=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)

	def __str__(self):
		return "Name: "+str(self.employee_firstname)+" Usernmae: "+str(self.user.username)+" Temp pass: "+str(self.employee_secondname)
	pass


# handle this 
# make sure that one cannot delete a store
class Item(SoftDeleteModel):
	store=models.ForeignKey(Store,on_delete=models.CASCADE)
	item_name=models.CharField(max_length=40,)
	item_price=models.FloatField( null=True,default=10000)
	# this is the number of items for single packages items, but for any other kind of package, you multiply per package and package quantity to get this item size field
	item_size=models.FloatField(null=True,blank=True)
	item_color=models.CharField(max_length=40,null=True,blank=True)
	item_manufucture=models.CharField(max_length=50,null=True,blank=True)
	item_discount=models.FloatField(null=True,blank=True)
	item_package_name=models.CharField(max_length=20,null=True,blank=True,default="single")
	item_package_quantity=models.FloatField(blank=True,null=True)
	item_per_package=models.FloatField(null=True,blank=True)
	item_minimum_allowed_quantity=models.FloatField(null=True,blank=True,default=20)
	is_active=models.BooleanField(default=True)
	item_image=models.ImageField(null=True,blank=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


	# objects=ItemManager()
	# items=ItemManager()

	def __str__(self):
		return str(self.item_name)+" "+str(self.item_color)


	def save(self,*args,**kargs):
		print('save')
		if self.item_manufucture is None or '':
			self.item_manufucture='oceanic'
		if self.item_price is None or '':
			self.item_price=300000
		if self.item_discount is None or '':
			self.item_discount=20
		if self.item_package_quantity is None or '':
			self.item_package_quantity=1
		if self.item_per_package is None or '':
			self.item_per_package=self.item_size
		if self.item_minimum_allowed_quantity is None or '':
			self.item_minimum_allowed_quantity=10
		
		super(Item,self).save(*args,**kargs)

	class Meta:
		ordering=['item_name']

# currently not used
class Inventory(SoftDeleteModel):
	# userid
	item=models.ForeignKey(Item,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	quantity=models.FloatField()
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


	def __str__(self):
		return str(self.quantity)
	pass

# deactivate user instad of deleting
# set active property on items and customer also
# 	make sure you handle creation, with consideration on deactive items, if items have the same names instead of creating new ones just activate the deleted one, this will help with space management
# 	the same applies to customers

class Sales(SoftDeleteModel):
	item=models.ForeignKey(Item,on_delete=models.CASCADE)
	# user here is the saler
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	# user here is the sales authorizer
	adminuser=models.IntegerField(null=True,blank=True)
	#user here is the one who releases the item sold
	issueuser=models.IntegerField(null=True,blank=True)
	customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
	sales_quantity=models.FloatField()
	sales_amount=models.FloatField()
	# sales_balance is used to hold loans , then updates sales_amount on payment 
	sales_balance=models.FloatField(default=0)
	sales_loan=models.BooleanField(default=True)
	sales_method_payment=models.CharField(max_length=10,default="cash")
	sales_piad_with_customer_credit=models.BooleanField(default=False)
	# sets pending for saler
	sales_received=models.BooleanField(default=False)
	#admin verifies the sale
	sales_authorized=models.BooleanField(default=False)
	#godown isues the item(s) sold
	sales_issue_item=models.BooleanField(default=False)
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)


	def __str__(self):
		return "Name:"+str(self.item.item_name)+" : Amount:"+str(self.sales_amount)+" :Balance"+str(self.sales_balance)+' method: '+str(self.sales_method_payment)

	class Meta:
		ordering=['-id']


class Account(SoftDeleteModel):
	account_name=models.CharField(max_length=20)
	account_user=models.ForeignKey(User,on_delete=models.CASCADE)
	account_company=models.ForeignKey(Company,on_delete=models.CASCADE)
	account_amount=models.FloatField()
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return str(self.account_name)


class Expense(SoftDeleteModel):
	expense_user=models.ForeignKey(User,on_delete=models.CASCADE)
	expense_account=models.ForeignKey(Account,on_delete=models.CASCADE)
	expense_item=models.CharField(max_length=40,default='expense')
	expense_receiver=models.CharField(max_length=40,default='receiver')
	# description is to imply why spend
	expense_description=models.TextField(null=True,blank=True)
	expense_amount=models.FloatField()
	created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
	updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)

	def __str__(self):
		return str(self.expense_description)

	
	class Meta:
		ordering=['-id']


# class Meta:
# 	odering = '-id'


