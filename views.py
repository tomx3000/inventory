from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.contrib import messages


from .models import Sales,Store,Employee,Company,Customer,Inventory,Item
from .forms import ItemForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.

pathselector={1:'base',2:'base',3:'order',4:'expense',5:'counter'}

privillage={'sales':3,'admin':1,'assistantadmin':2,'bursar':4,'godown':5}

@csrf_exempt
def AcceptSale(request,*args,**kargs):
	
	sale=Sales.objects.filter(id=kargs['id'])
	updatesale=sale.update(sales_received=True)
	# updating the quantity of item sold 

	item=Item.objects.filter(id=sale.first().item.id)
	item.update(item_size=item.first().item_size-sale.first().sales_quantity)

	print(kargs['id'])
	# print(request.POST)
	return HttpResponse('ok')

@csrf_exempt
def AuthorizeSale(request,*args,**kargs):
	
	sale=Sales.objects.filter(id=kargs['id'])
	updatesale=sale.update(sales_authorized=True,adminuser=request.user.id)

	# updating the quantity of item sold 
	print(kargs['id'])
	# print(request.POST)
	return HttpResponse('ok')

@csrf_exempt
def IssueSale(request,*args,**kargs):
	
	sale=Sales.objects.filter(id=kargs['id'])
	updatesale=sale.update(sales_issue_item=True,issueuser=request.user.id)

	# updating the quantity of item sold 
	print(kargs['id'])
	# print(request.POST)
	return HttpResponse('ok')

@csrf_exempt
def AcceptSaleAll(request,*args,**kargs):
	sales=Sales.objects.filter(sales_received=False)
	if sales.exists() and sales.count()>=1:
		for sale in sales:
			sale.sales_received=True
			sale.save()
			# updating the quantity of item sold 
			item=Item.objects.filter(id=sale.item.id)
			item.update(item_size=item.first().item_size-sale.sales_quantity)

	return HttpResponse('ok')

@csrf_exempt
def DeclineSaleAll(request,*args,**kargs):
	
	Sales.objects.filter(sales_received=False).delete()
	
	return HttpResponse('ok')

class MyView(View):
	def get(self,request,*args,**kagrs):
		return HttpResponse('hello CBV')

	def post(self,request,*args,**kagrs):
		print(request.POST['customer'])
		item=Item.objects.filter(id=request.POST['item'])
		customer=Customer.objects.filter(id=1)
		sale_order=Sales.objects.create(sales_quantity=request.POST['sales_quantity'],sales_amount=request.POST['sales_amount'],item=item,user=request.user,customer=customer)

		sale_order.save()
		return HttpResponse('ok')
class HomePage(View):
	def get(self,request,*args,**kagrs):
		form=ItemForm()

		user = request.user
		# home page limited to only admin 1 and 2
		if request.user.employee.employee_privillage <= privillage['assistantadmin']:
			return render(request,'home/base.html',{'form':form,'user':user})
		else:
			return redirect(pathselector[request.user.employee.employee_privillage])


def ViewOrder(request,*args,**kargs):

	user = request.user
	# access to the order/sales page limited to admin 1 and 2 and sales person 3
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['sales']:
		return render(request,'inventory/homepage.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])

		


def ViewProduct(request,*args,**kargs):
	user = request.user
	
	# access to item creation page limited to admin 1 and 2
	if request.user.employee.employee_privillage <= privillage['assistantadmin']:
		return render(request,'inventory/product.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])

def ViewCustomer(request,*args,**kargs):
	user = request.user
	# access to the order/sales page limited to admin 1 and 2 and sales person 3
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['sales']:
		return render(request,'inventory/customer.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])

def ViewCounter(request,*args,**kargs):

	user = request.user
	
	# access to item inventory/godown page limited to admin 1 and 2
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['godown']:
		return render(request,'inventory/inventory.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])


def ViewSettings(request,*args,**kargs):

	# less than 2 is admin
# just testing 
#  real <=2 i.e <= ssistantadmin
	if request.user.employee.employee_privillage >=1:
		return render(request,'inventory/settings.html',{})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])



def ViewExpense(request,*args,**kargs):

	user = request.user
	
	# access to item inventory/godown page limited to admin 1 and 2
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['bursar']:
		return render(request,'inventory/bursar.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])



	
def ViewLogin(request,*args,**kargs):
	form=ItemForm()
	if(request.method=='POST'):

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:

		    login(request, user)

		    # logout(request)
		    return redirect('base')

		else:
			return render(request,'inventory/login.html',{'form':form})	

	elif(request.method=='GET'):
		return render(request,'inventory/login.html',{'form':form})		

	
def ViewAuthorize(request,*args,**kargs):

	# less than 2 is admin

	if request.user.employee.employee_privillage <=privillage['assistantadmin']:
		return render(request,'inventory/authorize.html',{})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])


# print(args)
	# print(kagrs)

	# method one
	# try :
	# 	obj = Item.objects.get(color=kagrs['color'])
	# except:
	# 	obj=Item.objects.all().first()

	# method 2
	# qs=Item.objects.filter(color=kagrs['color'])
	# if qs.exists() and qs.count()>=1:
	# 	obj=qs.first()
	
	# method 3
	# obj=get_object_or_404(Item,id=color)
	# obj_color=obj.item_name
	# # print(request.method)
	# sales=Sales.objects.filter(id=request.POST['id'])
	



		# sales=Sales.objects.filter(sales_received=False)
	# if sales.exists() and sales.count()>=1:	
	# 	for sale in sales:
	# 		sale.update(sales_received=True)
	# else:
	# 	sales.update(sales_received=True)

