from django.shortcuts import render,redirect,reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm,ItemAdd,AssignItem
from .models import Employee,Item,ItemAssign,SellItems
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.mail import EmailMessage
from the_techbox import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .tasks import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import permissions
from .serializers import Item_Serializer,ItemAssignSerializer
from apps.product import signals 
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
import stripe
from django.conf import settings
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class Index(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self, request):
        form = EmployeeForm
        item_count = Item.objects.all().count()
        emp = Employee.objects.all().count()
        assign_item = ItemAssign.objects.all().count()
        avilable = (int(item_count) - int(assign_item))
        data = {
            'item_count':item_count,
            'emp':emp,
            'form':form,
            'assign_item': assign_item,
            'avilable':avilable
        }
        return render(request,'index.html',data)

    def post(self,request):
        emp = EmployeeForm(request.POST) 
        if emp.is_valid():
            name = request.POST['name']
            designation = request.POST['designation']
            email = request.POST['email']
            mobile = request.POST['mobile']
            usr = Employee(name=name,designation=designation,email=email,mobile=mobile)
            usr.save()
            messages.success(request,'Employee added successful')
        else:
            messages.error(request,'Email already in use')    
            return redirect('home')
        messages.success(request,'Employee added successful')
        return redirect('emplist')

class EmpListView(View):
    def get(self, request):
        emp  = Employee.objects.all()
        return render(request,'dashboard/employedata.html',{'emp':emp})


class AddEmployee(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self,request, pk=None):
        emp = EmployeeForm()
        return render(request,'dashboard/addemployee.html',{'emp':emp})

    def post(self,request):
        emp = EmployeeForm(request.POST) 
        if emp.is_valid():
            name = request.POST['name']
            designation = request.POST['designation']
            email = request.POST['email']
            mobile = request.POST['mobile']
            usr = Employee(name=name,designation=designation,email=email,mobile=mobile)
            usr.save()
            messages.success(request, 'Employee added successful')
        else:
            messages.error(request,'Email already in use')    
        return redirect('emplist')

class EmpUpdate(UpdateView):
    @method_decorator(login_required(login_url="/login/"))
    def get(self, request, pk):
        emp = Employee.objects.get(pk=pk)
        form = EmployeeForm(instance=emp)
        return render(request, 'dashboard/empupdate.html', {'form': form})

    def post(self, request, pk):
        emp = Employee.objects.get(id=pk)
        emp_update = EmployeeForm(request.POST, instance=emp)
        if emp_update.is_valid():
            emp_update.save()
        else:
            messages.error(request,'Data not Vailid') 
        return redirect('emplist')
        

class EmpDelete(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self,request,pk):
        emp = Employee.objects.get(pk=pk)
        emp.delete()
        return redirect('emplist')

@method_decorator(cache_page(60), name='dispatch')
# @method_decorator(login_required(login_url="/login/"))
class ItemListView(View):
    def get(self,request):
        item = Item.objects.all()
        item_add = ItemAdd()
        return render(request,'dashboard/item.html',{'items':item,'item_add':item_add,})

    def post(self,request):
        item = ItemAdd(request.POST or None)
        items = request.POST['name']
        if item.is_valid():
            item.save()
            signals.notification.send(sender=None, items = items)
            messages.success(request, 'Added successful')  
        else:
            messages.error(request,'Unable to added')    
        return redirect('itemlist')

class ItemDelete(View):
    @method_decorator(login_required(login_url="/login/"))
    def post(self, request):
        item_id = request.POST.get('id')
        item = Item.objects.get(id=item_id)
        item.delete()
        return redirect('itemlist')

class ItemAssigns(View):
    def get(self, request):
        item = AssignItem
        items = ItemAssign.objects.all()
        return render(request,'dashboard/itemassign.html',{'item':item,'items':items})
    def post(self, request):
        item = AssignItem(request.POST or None)
        uid = request.POST['assign_to']
        iid = request.POST['assign_item']
        emp = Employee.objects.get(id=uid)
        emails = emp.email
        borrow = Item.objects.get(id=iid)
        items = Item.objects.all().count()
        given_item = ItemAssign.objects.all().count()
        if borrow.status == False:
            messages.success(request,'Following item is out of stock')
        elif given_item > items or (given_item) == (items):
            messages.success(request,'item is not avilable')
        else:   
            if item.is_valid():
                item.save()
                borrow = str(borrow)
                send_emails.delay(emails,borrow)
                messages.success(request, 'Assign successful mail send to employee')
            else:
                messages.error(request,'Unable to Assign')    
        return redirect('item-assign')

class ItemAssignsDelete(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self,request,pk):
        item = ItemAssign.objects.get(pk=pk)
        item.delete()
        return redirect('item-assign')


class ItemListApiView(APIView):
    # 1. Get
    def get(self,request,pk=None):
        id = pk
        try:
            if id is not None:
                items = Item.objects.get(id=id)
                serializer = Item_Serializer(items)
                return Response(serializer.data, status=status.HTTP_200_OK)
            items = Item.objects.all()
            serializer = Item_Serializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    # 2. Create
    def post(self, request, *args, **kwargs):
        serializer = Item_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #3. PUT
    def put(self,request,pk):
        id = pk
        items = Item.objects.get(id=id)
        serializer = Item_Serializer(items,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        id = pk
        try:
            if id is not None:
                items = Item.objects.get(id=id)
                items.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ItemAssignApiView(viewsets.ModelViewSet):
    queryset = ItemAssign.objects.all()
    serializer_class = ItemAssignSerializer


class PurchasePage(View):
    def get(self, request):
        return render(request, 'dashboard/purchase.html')

class Charge(View):
    def post(self, request):
        # import pdb; pdb.set_trace()
        amount = int(request.POST['amount'])
        name = request.POST['uname']
        email = request.POST['email']
        customer = stripe.Customer.create(
                name=name,
                email=email,
                source=request.POST['stripeToken'],
            )
        charge = stripe.Charge.create(
            customer=customer,
            amount= int(amount)*100,
            currency='inr',
            description="Testing amount"
        )
        return redirect(reverse('success'))

class Success(View):
    def get(self, request):
        return render(request, 'dashboard/success.html')