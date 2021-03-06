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
from django.db.models import Count, F, Value

import csv
# Create your views here.

pathselector={1:'base',2:'base',3:'order',4:'expense',5:'counter'}

privillage={'sales':3,'admin':1,'assistantadmin':2,'bursar':4,'godown':5}
# hnishael@gmail.com

import datetime
from inventory.utils import render_to_pdf ,render_to_pdf_with_image #created in step 4
from django.template.loader import get_template
from django.db.models import Sum
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Avg,Sum
from datetime import timedelta
from django.utils import timezone

def delete_recovery(object):
	pass

def soft_delete(object):
	pass

def check_correct_uniqueness():
	# list for holding the customers' names while going throught them in the database
	tempcustomer=[]

	# using raw query so as to by bass the deliberate limitation that were overidden in the model class of not getting all the rows within an entitty 

	# getting all customers, deleted(dead) and not deleted( alive)
	customers = Customer.objects.raw('select * from inventory_customer where deleted_at is not null or deleted_at is null')

	# going through the customers
	for index,customer in enumerate(customers):
		print("Customer: "+str(index))
		# check if the list contains a customer name
		if tempcustomer.__contains__(customer.customer_name):
			# if yes
			# modify the customer name and store it temporarly
			new_customer_name=customer.customer_name+str(tempcustomer.count(customer.customer_name))

			count=0

			# check if the newly modifed customer is in the list also
			while(tempcustomer.__contains__(new_customer_name)):
				# if yes modify the new customer name till its is not found in the list
				new_customer_name=new_customer_name+str(count)
				count+=1

			# now add the new customer name to the customer list
			tempcustomer.append(new_customer_name)
			# modify the customer name in the database to the new customer name
			customer.customer_name=new_customer_name
			# save the customer 
			customer.save()
			
		else:
			# if customer name not in list 
			# add it to the customer list
			tempcustomer.append(customer.customer_name)

	print('done')


@csrf_exempt
@login_required(login_url='/login/')
def getGraphBata(request, *args, **kargs):
	# check_correct_uniqueness()
	print('graph')
	days_dict={1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Sartuday',7:'Sunday'}

	def deltaSelect(day):
		delta=datetime.date.today().isocalendar()[2]-day
		print(delta)
		if delta<0:
			print(delta)
			delta=7+delta
		return delta

	sunday=datetime.date.today()-timedelta(days=deltaSelect(0))
	monday=datetime.date.today()-timedelta(days=deltaSelect(1))
	tuesday=datetime.date.today()-timedelta(days=deltaSelect(2))
	wednesday=datetime.date.today()-timedelta(days=deltaSelect(3))
	thursday=datetime.date.today()-timedelta(days=deltaSelect(4))
	friday=datetime.date.today()-timedelta(days=deltaSelect(5))
	sartuday=datetime.date.today()-timedelta(days=deltaSelect(6))
	
	sunday_sales=Sales.objects.filter(created_at__gte=sunday,created_at__lt=sunday+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	monday_sales=Sales.objects.filter(created_at__gte=monday,created_at__lt=monday+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	tuesday_sales=Sales.objects.filter(created_at__gte=tuesday,created_at__lt=tuesday+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	wednesday_sales=Sales.objects.filter(created_at__gte=wednesday,created_at__lt=wednesday+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	thursday_sales=Sales.objects.filter(created_at__gte=thursday,created_at__lt=thursday+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	friday_sales=Sales.objects.filter(created_at__gte=friday,created_at__lt=friday+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	sartuday_sales=Sales.objects.filter(created_at__gte=sartuday,created_at__lt=sartuday+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	print('today')
	print(datetime.datetime.now())
	print('iso calender position for today')
	print(datetime.date.today().isocalendar()[2])

	today_sales=Sales.objects.filter(created_at__gte=datetime.date.today(),created_at__lt=datetime.date.today()+timedelta(days=1)).aggregate(Sum('sales_amount'))['sales_amount__sum']
	print('today\'s date:{}'.format(datetime.date.today()))
	print('today:{}'.format(today_sales))
	print('Date monday:{}'.format(monday))
	print("Sales monday:{}".format(monday_sales))
	print('Date tuesday:{}'.format(tuesday))
	print("Sales tuesday:{}".format(tuesday_sales))
	print('Date wednesday:{}'.format(wednesday))
	print("Sales wednesday:{}".format(wednesday_sales))
	print('Date thursday:{}'.format(thursday))
	print("Sales thursday:{}".format(thursday_sales))
	print('Date friday:{}'.format(friday))
	print("Sales friday:{}".format(friday_sales))
	print('Date sartuday:{}'.format(sartuday))
	print("Sales sartuday:{}".format(sartuday_sales))
	print('Date sunday:{}'.format(sunday))
	print("Sales sunday:{}".format(sunday_sales))
	
	data_to_display=arrrange_days_forgraph(days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sartuday","Sunday"],data=[monday_sales,tuesday_sales,wednesday_sales,thursday_sales,friday_sales,sartuday_sales,sunday_sales])

	data = {
	  'data': data_to_display["values"],

	 'label':data_to_display["days"],
	 'order_id': 1233434,
	}
	
	return JsonResponse(data)


def arrrange_days_forgraph(data=None,days=None):
	days_value=[]
	arranged_days=[]
	
	days_position=[]	
	# getting sequence of the previous days
	for index in range(7):
		days_position.append((datetime.date.today()-timedelta(days=index)).isocalendar()[2])

	print("position of says in sequence")
	print(days_position)	

	# arranging the days in appropriate sequence
	for position in days_position:
		print(position)
		arranged_days.append(days[position-1])

	print("new arranged days")
	print(list(reversed(arranged_days)))

	# the values in appropiate sequence
	for position in days_position:
		print(position)
		if data[position-1] is None:
			data[position-1]=0
			print(0)
		days_value.append(data[position-1])

	print("new arranged data")
	print(list(reversed(days_value)))

	# define a function that goes down to zero from today's iso value

	# define a function that goes down to todays iso value from the maximum value

	# oneach funciton append the values to the approrpiacte list for return to the frontend graph for drawing 

	return {"days":list(reversed(arranged_days)),"values":list(reversed(days_value))}
	


@csrf_exempt
@login_required(login_url='/login/')
def OrderPdf(request, *args, **kwargs):
	print('oldpdf')

	data = {
	  'today': datetime.date.today(), 
	  'amount': 39.99,
	 'customer_name': 'Cooper Mann',
	 'order_id': 1233434,
	}

	pdf = render_to_pdf('inventory/pdforder.html', data)
	return HttpResponse(pdf, content_type='application/pdf')


@csrf_exempt
@login_required(login_url='/login/')
def OrderPdf_Auto(request, *args, **kwargs):
	customer=Customer.objects.get(id=kwargs['id'])
	if request.user.employee.employee_privillage<=privillage['assistantadmin']:
		sales=Sales.objects.filter(Q(sales_authorized=False )|Q(sales_method_payment='loan'),customer=customer)
	else:
		user=request.user

		sales=Sales.objects.filter(sales_received=False,user=request.user,customer=customer)
	employee= Employee.objects.get(user=request.user)
	items = Item.objects.all()
	total=sales.aggregate(Sum('sales_amount'))
	print(total)

	print('custoemrid')
	print(kwargs['id'])
	template = get_template('inventory/pdforder.html')
	context = {
	"logo":"/static/inventory/oceanicpicjpg.png",
	 "order_id": 123,
	 "customer_name": "John Cooper",
	 "amount": 1399.99,
	 "today": datetime.date.today(),
	 'orders':sales,
	 'customer':customer,
	 'items':items,
	 'employee':employee,
	 'amount':'Tsh {:,.2f}'.format(total['sales_amount__sum']),
	}

	html = template.render(context)
	pdf = render_to_pdf_with_image('inventory/pdforder.html', context)

	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "{}_{}_Order.pdf".format(customer.customer_name,datetime.date.today())
		content = "inline; filename='%s'" %(filename)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response
	return HttpResponse("Not found")


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

	# email=admin.first().employee_email

	email=User.objects.get(id=request.user.id).employee.employee_email
	

	# sending login credential to admin or user them selves
	send_mail(
		    'Resetin Password',
		    'OCEANIC \n firstname :'+employee.employee_firstname+'\n'+'username :'+user.username+'\n password: '+password,
		    'info.company.tz@gmail.com',
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
			try:

				existimg_customer,new_customer=Customer.objects.get_or_create(company=Company.objects.get(id=request.POST['company']),customer_name=fields[0],customer_phone=fields[2],customer_location=fields[1])
			except Exception as e:
				print('error: {}'.format(e))
				continue
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

# remeber the best way to implemet a sale order and handling loans is by implementing a whole new order table linked to the sales table 
# due to the sake of time and inconvinience a hack around is implemented by navingating some boolean fields in the sales table and paymet_methods column and balaance column is added for this exact purpose
# in future a much more simpler implementation should eliminate this processing bottleneck

@csrf_exempt
@login_required(login_url='/login/')
def restoreCustomerCredit(request,*args,**kargs):
	customer=Customer.objects.get(id=kargs['customerid'])
	sale=Sales.objects.get(id=kargs['saleid'])

	# if customer has a crdit balance 
	#  you can restore the amount 
	if (sale.sales_piad_with_customer_credit):
		print("credit restore amount")
		print(round(float(kargs['amount'])))
		customer.customer_debit_amount+=round(float(kargs['amount']))
		customer.save()


	return HttpResponse('ok')



@csrf_exempt
@login_required(login_url='/login/')
def UpdateCustomerSalesPaymentMethodAuth(request,*args,**kargs):
	# customer loan acceptance code
	customer=Customer.objects.get(id=kargs['customerid'])
	# note cash here means the payment method
	print("method:"+kargs['cash'])

	customer_loan_order=Sales.objects.filter(customer=customer,sales_method_payment="loan")

	customer_order_loan_balance=customer_loan_order.aggregate(Sum('sales_balance'))['sales_balance__sum']

	number_of_sales_in_orders=customer_loan_order.count()

	def isCreditFree(amountpaid,totalbalance):
		free =False
		extra_cash_paid=0
		if amountpaid >= round(totalbalance):
			free=True
			extra_cash_paid=amountpaid-round(totalbalance)
		return [free,extra_cash_paid]

	if isCreditFree(float(kargs['amount']),customer_order_loan_balance)[0]:
		updatedsales=customer_loan_order.update(sales_method_payment=kargs['cash'],sales_balance=F('sales_amount'))

		# record that customer has paid extra

		# adding current extra customer amount to the new extra 
		customer.customer_debit_amount+=isCreditFree(float(kargs['amount']),customer_order_loan_balance)[1]
		customer.save()

		print('no more loan')
	else:
		current_balance=round(customer_order_loan_balance)-float(kargs['amount'])
		# the actual hack
		# i save the total loan balance in each order item equally distributing it, for later reconstruction
		balance_per_sale=current_balance/number_of_sales_in_orders

		updatedsales=customer_loan_order.update(sales_balance=balance_per_sale)
		print('balance to be paid')
		print(current_balance)
		print('updated balance')
		print(balance_per_sale)
		print('updated end')

	return HttpResponse('ok')


@csrf_exempt
@login_required(login_url='/login/')
def UpdateSalesPaymentMethodAuth(request,*args,**kargs):
	print('taking loan')
	sale=Sales.objects.get(id=kargs['saleid'])
	print('amount paid')
	print(float(kargs['amount']))
	balance=sale.sales_balance-float(kargs['amount'])
	sale.sales_balance=balance
	print('balance')
	print(balance)
	if balance<=0:
		sale.sales_method_payment=kargs['cash']

	sale.save()
	# updating the quantity of item sold 
	print(kargs['saleid'])
	# print(request.POST)
	return HttpResponse('ok')


@csrf_exempt
@login_required(login_url='/login/')
def UpdateSalesPaymentMethod(request,*args,**kargs):
	print('geting single loan')
	sale=Sales.objects.filter(id=kargs['saleid'])
	amount=0
	updatesale=sale.update(sales_method_payment=kargs['cash'],sales_balance=F('sales_amount'))

	# updating the quantity of item sold 
	print(kargs['saleid'])
	# print(request.POST)
	return HttpResponse('ok')

@csrf_exempt
@login_required(login_url='/login/')
def UpdateCustomerSalesPaymentMethod(request,*args,**kargs):
	customer=Customer.objects.get(id=kargs['customerid'])
	amount=0
	print('multiplesss...')
	print(kargs['cash'])

	# begin handling of customer credit balance

	if customer.customer_debit_amount>0:
		# custoemr has credit balance

		# getting total sales for a customer's order
		customer_total_order=Sales.objects.filter(customer=customer,sales_received=False).aggregate(Sum('sales_amount'))['sales_amount__sum']

		# deducting the credit balance from amount paid for the order

		customer_total_order-=customer.customer_debit_amount

		# getting total number of items within the customer order
		number_of_items_in_order=Sales.objects.filter(customer=customer,sales_received=False).count()

		if customer_total_order <0:
			# customer still has credit balance
			customer.customer_debit_amount=(-1)*customer_total_order
			# reseting the customer total order
			customer_total_order=0

			# update each individual sales balance to zero
			updatesale=Sales.objects.filter(customer=customer,sales_received=False).update(sales_method_payment=kargs['cash'],sales_balance=0,sales_piad_with_customer_credit=True)
			print("customer credit remains: ",customer_total_order*-1)

		else:
			# customer no longer has credit balance
			customer.customer_debit_amount=0

			# to store the order amount modified by the credit balance, we split the resultant amount into individual units and stroe each unit balance into respective sale within the customers order
			
			balance_per_item=round(customer_total_order/number_of_items_in_order)

			# update the customer sales order with this neer balnce  on each item within the order

			updatesale=Sales.objects.filter(customer=customer,sales_received=False).update(sales_method_payment=kargs['cash'],sales_balance=balance_per_item,sales_piad_with_customer_credit=True)

			print("balance per item ", balance_per_item)

		customer.save()

	else:
		updatesale=Sales.objects.filter(customer=customer,sales_received=False).update(sales_method_payment=kargs['cash'],sales_balance=F('sales_amount'))

		
	# end handling of credit balance
	
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




