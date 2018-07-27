from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.contrib import messages


from .models import Sales,Store,Employee,Company,Customer,Inventory,Item,Account,Expense
from .forms import ItemForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.contrib.auth.mixins import LoginRequiredMixin
import csv
# Create your views here.

pathselector={1:'base',2:'base',3:'order',4:'expense',5:'counter'}

privillage={'sales':3,'admin':1,'assistantadmin':2,'bursar':4,'godown':5}
# hnishael@gmail.com

@csrf_exempt
@login_required(login_url='/login/')
def resetPassword(request,*args,**kargs):

	user= User.objects.get(id=kargs['id'])

	print('gotcha create something')
	import random
	import string

	def generateRoandom(size=4,chars=string.ascii_lowercase+string.ascii_uppercase+string.digits):

		return ''.join(random.choice(chars) for _ in range(size))

	password=generateRoandom(8)

	user.set_password(password)
	user.save()
	employee=Employee.objects.get(user=user.id)

	admin = Employee.objects.filter(employee_privillage=1)
	email=admin.first().employee_email
		


	# sending login credential to admin or user them selves
	send_mail(
		    'Resetin Password',
		    'OCEANIC \n firstname :'+employee.employee_firstname+'\n'+'username :'+user.username+'\n password: '+password,
		    'tomx3000@gmail.com',
		    [email],
		    fail_silently=False,
		   
		)

	return HttpResponse('done')


@csrf_exempt
@login_required(login_url='/login/')
def ChangePassword(request,*args,**kargs):
	user = authenticate(request, username=kargs['username'], password=kargs['oldpassword'])

	if user is not None:

		if kargs['firstnewpassword'] == kargs['secondnewpassword']:		
			user.set_password(kargs['firstnewpassword'])
			user.save()
			return HttpResponse('good')
		else:
			return HttpResponse('notmatched')

	else:
		return HttpResponse('badold')

@csrf_exempt
@login_required(login_url='/login/')
def ChangeUsername(request,*args,**kargs):
	try:
		user=User.objects.get(username=kargs['username'])

	except Exception as e:
		User.objects.filter(id=kargs['id']).update(username=kargs['username'])
		return HttpResponse('good')
	else:
		return HttpResponse('bad')


@csrf_exempt
@login_required(login_url='/login/')
def ItemFile(request,*args,**kargs):

	# with open(request.FILES['file'],'r') as csv_file:
	csv_file=request.FILES['file']
	print(csv_file.name.endswith('csv'))

	file_data=csv_file.read().decode('utf-8')
	lines=file_data.split('\n')
	# line_dict=get_lines_dict(lines)

	# work on this function so as to allow flexibility of csv upload
	for counter, line in enumerate(lines):
		if counter is 0 :
			continue
		fields=line.split(',')
		
		if(len(fields)<2):
			print(fields)
		else:
			print(counter)
			existimg_item,new_item=Item.objects.get_or_create(store=Store.objects.get(id=request.POST['store']),item_name=fields[0],item_size=fields[1])
			# new_customer.save()
	print("done , items stored")
	return HttpResponse('ok')



@csrf_exempt
@login_required(login_url='/login/')
def CustomerFile(request,*args,**kargs):

	# with open(request.FILES['file'],'r') as csv_file:
	csv_file=request.FILES['file']
	print(csv_file.name.endswith('csv'))

	file_data=csv_file.read().decode('utf-8')
	lines=file_data.split('\n')
	# line_dict=get_lines_dict(lines)

	# work on this function so as to allow flexibility of csv upload
	for counter, line in enumerate(lines):
		if counter is 0 :
			continue
		fields=line.split(',')
		
		if(len(fields)<3):
			print(fields)
		else:
			print(counter)
			existimg_customer,new_customer=Customer.objects.get_or_create(company=Company.objects.get(id=request.POST['company']),customer_name=fields[0],customer_phone=fields[2],customer_location=fields[1])
			# new_customer.save()
	print("Done, Customers stores")
	return HttpResponse('ok')
	
def get_lines_dict(file_lines):
	atributes_dict={}
	lines_dict={}
	for index,line in enumerate(file_lines):
		if index is 0:
			fields= line.split(',')
			for pos,field in enumerate(fields):
				atributes_dict[pos]=field
				lines_dict[field]=[]

			break

	
	for index,line in enumerate(file_lines):
		if index is not 0:
			cells = line.split(',')

			for pos,cell in enumerate(cells):
				if len(cell)>1:
					lines_dict[atributes_dict[pos]].append(cell)


				
	print(lines_dict)
	return lines_dict


@csrf_exempt
@login_required(login_url='/login/')
def increaseAccount(request,*args,**kargs):
	account=Account.objects.filter(id=kargs['id'])
	account.update(account_amount=float(account.first().account_amount)+float(kargs['amount']))
	return HttpResponse('ok')


@csrf_exempt
@login_required(login_url='/login/')
def decreaseAccount(request,*args,**kargs):
	account=Account.objects.filter(id=kargs['id'])
	account.update(account_amount=float(account.first().account_amount)-float(kargs['amount']))
	return HttpResponse('ok')

@csrf_exempt
@login_required(login_url='/login/')
def updateUpDownAccount(request,*args,**kargs):
	expense=Expense.objects.filter(id=kargs['id'])

	account=Account.objects.filter(id=expense.first().expense_account.id)
	account.update(account_amount=float(account.first().account_amount)-(float(kargs['amount'])-float(expense.first().expense_amount)))
	print('current expense amount')
	print(float(expense.first().expense_amount))
	print('entered value')
	print(float(kargs['amount']))
	print('balance')
	print(float(account.first().account_amount))
	print('adjusted balance')
	adjustedval=float(account.first().account_amount)-(float(kargs['amount'])-float(expense.first().expense_amount))
	print(adjustedval)
	print(kargs['id'])

	# print(request.POST)
	return HttpResponse(adjustedval)

@csrf_exempt
@login_required(login_url='/login/')	
def increseItem(request,*args,**kargs):
	item=Item.objects.filter(id=kargs['id'])
	item.update(item_size=float(item.first().item_size)+float(kargs['quantity']))
	return HttpResponse('ok')
	

@csrf_exempt
@login_required(login_url='/login/')
def decreaseItem(request,*args,**kargs):
	item=Item.objects.filter(id=kargs['id'])
	item.update(item_size=float(item.first().item_size)-float(kargs['quantity']))
	return HttpResponse('ok')


@csrf_exempt
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
def UpdateSalesPaymentMethod(request,*args,**kargs):
	
	sale=Sales.objects.filter(id=kargs['saleid'])
	updatesale=sale.update(sales_method_payment=kargs['cash'])

	# updating the quantity of item sold 
	print(kargs['saleid'])
	# print(request.POST)
	return HttpResponse('ok')

@csrf_exempt
@login_required(login_url='/login/')
def UpdateCustomerSalesPaymentMethod(request,*args,**kargs):
	customer=Customer.objects.get(id=kargs['customerid'])

	sale=Sales.objects.filter(customer=customer,sales_received=False).update(sales_method_payment=kargs['cash'])

	return HttpResponse('ok')

@csrf_exempt
@login_required(login_url='/login/')
def AuthorizeCustomerOrder(request,*args,**kargs):
	customer=Customer.objects.get(id=kargs['customerid'])

	sale=Sales.objects.filter(customer=customer,sales_received=True,sales_authorized=False).update(sales_authorized=True,adminuser=request.user.id)

	return HttpResponse('ok')



@csrf_exempt
@login_required(login_url='/login/')
def AuthorizeSale(request,*args,**kargs):
	
	sale=Sales.objects.filter(id=kargs['id'])
	updatesale=sale.update(sales_authorized=True,adminuser=request.user.id)

	# updating the quantity of item sold 
	print(kargs['id'])
	# print(request.POST)
	return HttpResponse('ok')


@csrf_exempt
@login_required(login_url='/login/')
def IssueCustomerOrder(request,*args,**kargs):
	customer=Customer.objects.get(id=kargs['customerid'])

	sale=Sales.objects.filter(customer=customer,sales_authorized=True,sales_issue_item=False).update(sales_issue_item=True,issueuser=request.user.id)

	return HttpResponse('ok')



@csrf_exempt
@login_required(login_url='/login/')
def IssueSale(request,*args,**kargs):
	
	sale=Sales.objects.filter(id=kargs['id'])
	updatesale=sale.update(sales_issue_item=True,issueuser=request.user.id)

	# updating the quantity of item sold 
	print(kargs['id'])
	# print(request.POST)
	return HttpResponse('ok')


@csrf_exempt
@login_required(login_url='/login/')
def AcceptCustomerOder(request,*args,**kargs):
	customer=Customer.objects.get(id=kargs['customerid'])
	sales=Sales.objects.filter(sales_received=False,customer=customer)
	if sales.exists() and sales.count()>=1:
		for sale in sales:
			sale.sales_received=True
			sale.save()
			# updating the quantity of item sold 
			item=Item.objects.filter(id=sale.item.id)
			item.update(item_size=item.first().item_size-sale.sales_quantity)

	return HttpResponse('ok')


@csrf_exempt
@login_required(login_url='/login/')
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
@login_required(login_url='/login/')
def DeclineCustomerOder(request,*args,**kargs):
	customer=Customer.objects.get(id=kargs['customerid'])
	sales=Sales.objects.filter(sales_received=False,customer=customer)
	if sales.exists() and sales.count()>=1:
		for sale in sales:
			# updating the quantity of item sold 
			item=Item.objects.filter(id=sale.item.id)
			item.update(item_size=item.first().item_size+sale.sales_quantity)
	
	Sales.objects.filter(sales_received=False,customer=customer).delete()
	
	return HttpResponse('ok')

@csrf_exempt
@login_required(login_url='/login/')
def DeclineSaleAll(request,*args,**kargs):
	sales=Sales.objects.filter(sales_received=False)
	if sales.exists() and sales.count()>=1:
		for sale in sales:
			# updating the quantity of item sold 
			item=Item.objects.filter(id=sale.item.id)
			item.update(item_size=item.first().item_size+sale.sales_quantity)
	
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



class HomePage(LoginRequiredMixin,View):
	login_url = '/login/'
	def get(self,request,*args,**kagrs):
		form=ItemForm()

		user = request.user
		# home page limited to only admin 1 and 2
		if request.user.employee.employee_privillage <= privillage['assistantadmin']:
			return render(request,'home/base.html',{'form':form,'user':user})
		else:
			return redirect(pathselector[request.user.employee.employee_privillage])





@login_required(login_url='/login/')
def ViewOrder(request,*args,**kargs):

	user = request.user
	# access to the order/sales page limited to admin 1 and 2 and sales person 3
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['sales']:
		return render(request,'inventory/homepage.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])

		

@login_required(login_url='/login/')
def ViewProduct(request,*args,**kargs):
	user = request.user
	
	# access to item creation page limited to admin 1 and 2
	if request.user.employee.employee_privillage <= privillage['assistantadmin']:
		return render(request,'inventory/product.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])



@login_required(login_url='/login/')
def ViewCustomer(request,*args,**kargs):
	user = request.user
	# access to the order/sales page limited to admin 1 and 2 and sales person 3
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['sales']:
		return render(request,'inventory/customer.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])



@login_required(login_url='/login/')
def ViewCounter(request,*args,**kargs):

	user = request.user
	
	# access to item inventory/godown page limited to admin 1 and 2
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['godown']:
		return render(request,'inventory/inventory.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])


@login_required(login_url='/login/')
def ViewSettings(request,*args,**kargs):

	# less than 2 is admin
# just testing 
#  real <=2 i.e <= ssistantadmin
	if request.user.employee.employee_privillage <=privillage['assistantadmin']:
		return render(request,'inventory/settings.html',{})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])


@login_required(login_url='/login/')
def ViewExpense(request,*args,**kargs):

	user = request.user
	
	# access to item inventory/godown page limited to admin 1 and 2
	if request.user.employee.employee_privillage <= privillage['assistantadmin'] or request.user.employee.employee_privillage == privillage['bursar']:
		return render(request,'inventory/bursar.html',{'user':user})
	else:
		return redirect(pathselector[request.user.employee.employee_privillage])

@login_required(login_url='/login/')
def ViewProfile(request,*args,**kargs):
	user = request.user
	
	return render(request,'inventory/profile.html',{'user':user})
	
	
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
			return render(request,'inventory/login.html',{})	

	elif(request.method=='GET'):
		logout(request)
		return render(request,'inventory/login.html',{'form':form})		


@login_required(login_url='/login/')
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


