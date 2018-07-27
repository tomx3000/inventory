from rest_framework import viewsets,filters
from .models import Sales,Store,Employee,Company,Customer,Inventory,Item,Account,Expense
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from django.core.mail import send_mail
from .serializers import SalesSerializer,StoreSerializer,CompanySerializer,EmployeeSerializer,CustomerSerializer,InventorySerializer,ItemSerializer,AccountSerializer,ExpenseSerializer,UserSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .csrfexempt import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User 
from django.contrib import messages

class SalesViewSet(viewsets.ModelViewSet):

	queryset=Sales.objects.all()
	serializer_class=SalesSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('customer__customer_name', 'item__item_name','sales_quantity','sales_amount','sales_method_payment','user__employee__employee_firstname','created_at','id')
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
                        


	# def list(self,request):
	# 	userid=request.user.id
	# 	# print(user)
	# 	# qs = Sales.objects.filter(user=user)

	# 	qs = Sales.objects.filter(id__gte=1,user=request.user)

	# 	serializer=SalesSerializer(qs,many=True)
	# 	return Response({'serial':serializer.data,'userid':userid})

	# overiding use of geting on value of sale to making it get all values of sale without considering user requesting it
	# def retrieve(self, request, pk=None):
	# 	userid=request.user.id

	# 	qs = Sales.objects.all()


	# 	serializer=SalesSerializer(qs,many=True)

	# 	return Response({'serial':serializer.data,'userid':userid})
        

	# @csrf_exempt
	# def creaate(self,request):
	# 	print('posted')
	# 	item=Item.objects.filter(id=request.POST['item'])
	# 	customer=Customer.objects.filter(id=1)
	# 	sale_order=Sales.objects.create(sales_quantity=request.POST['sales_quantity'],sales_amount=request.POST['sales_amount'],item=item,user=request.user,customer=customer)

	# 	return Response('serial')
	# def perform_create(self,serializer):
	# 	serializer.save(user=self.request.user)

class AccountViewSet(viewsets.ModelViewSet):
	queryset=Account.objects.all()
	serializer_class=AccountSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class UserViewSet(viewsets.ModelViewSet):
	queryset=User.objects.all()
	serializer_class=UserSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class ExpenseViewSet(viewsets.ModelViewSet):
	queryset=Expense.objects.all()
	serializer_class=ExpenseSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('expense_item', 'expense_description','expense_amount','expense_user__employee__employee_firstname','created_at')
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)


	# add get users expense 
	#  add get all expense


class StoreViewSet(viewsets.ModelViewSet):
	queryset=Store.objects.all()
	serializer_class=StoreSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	
class EmployeeViewSet(viewsets.ModelViewSet):
	queryset=Employee.objects.all()
	serializer_class=EmployeeSerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	def create(self,request):
		print('gotcha create something')
		import random
		import string

		def generateRoandom(size=4,chars=string.ascii_lowercase+string.ascii_uppercase+string.digits):

			return ''.join(random.choice(chars) for _ in range(size))

		user=None

		while(not user):
			username = request.data.get('employee_firstname')+''+generateRoandom(3)

			password=generateRoandom(8)
			email=request.data.get('employee_firstname')+'@gmail.com'
			user = User.objects.create_user(username, email, password)

		company=Company.objects.get(id=request.data.get('company'))

		employee=Employee.objects.create(user=user,company=company,employee_position=request.data.get('employee_position'),employee_privillage=request.data.get('employee_privillage'),employee_secondname=password,
			employee_firstname=request.data.get('employee_firstname'),employee_phone=request.data.get('employee_phone')
			)
		# print(request.data.get('employee_firstname'))
		
		# sending login credential to admin or user them selves
		admin = Employee.objects.filter(employee_privillage=1)
		email=admin.first().employee_email
		send_mail(
			    'NEWUSER',
			    'OCEANIC \n firstname :'+request.data.get('employee_firstname')+'\n'+'username :'+username+'\n password: '+password,
			    'tomx3000@gmail.com',
			    [email],
			    fail_silently=False,
			   	
			)

		return Response({'username':username,'password':'password'})

	def destroy(self,request,pk=None):
		User.objects.filter(id=Employee.objects.get(id=pk).user.id).delete()

		# return super().destroy(request)
		return Response('ok')



class CompanyViewSet(viewsets.ModelViewSet):
	queryset=Company.objects.all()
	serializer_class=CompanySerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

	def list(self,request):
		qs = Company.objects.filter(id__gte=1)

		serializer=CompanySerializer(qs,many=True)

		userid=request.user.id

		return Response({'serial':serializer.data,'userid':userid})


class CustomerViewSet(viewsets.ModelViewSet):
	queryset=Customer.objects.all()
	serializer_class=CustomerSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('customer_name', 'customer_phone','customer_location','customer_transport','created_at')
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class InventoryViewSet(viewsets.ModelViewSet):
	queryset=Inventory.objects.all()
	serializer_class=InventorySerializer
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)

class ItemViewSet(viewsets.ModelViewSet):

	queryset=Item.objects.all()
	serializer_class=ItemSerializer
	filter_backends = (filters.SearchFilter,)
	search_fields = ('item_name', 'item_price','item_size','item_manufucture')
	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	permission_classes=(permissions.IsAuthenticatedOrReadOnly,)




    
	




