from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection
from hashlib import md5
from report.models import *
from django.contrib import messages



def index(request):
    return render(request, 'home.html')


def customer(request):
    customer_code = request.GET.get('customer_code', '')
    customers = list(Customer.objects.filter(customer_code=customer_code).values())
    data = dict()
    data['customers'] = customers
    
    return render(request, 'login.html', data)

class ProductList(View):
    def get(self, request):
        products = list(Product.objects.all().values())
        data = dict()
        data['products'] = products

        return JsonResponse(data)

class CustomerList(View):
    def get(self, request):
        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)

class CustomerGet(View):
    def get(self, request, customer_code):
        customers = list(Customer.objects.filter(customer_code=customer_code).values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)        

@method_decorator(csrf_exempt, name='dispatch')
class CustomerSave(View):
    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers
        
        return render(request, 'login.html', data)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class CustomerSave2(View):
    def post(self, request):

        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['customers'] = list()
            return JsonResponse(ret)

        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class CustomerDelete(View):
    def post(self, request):

        customer_code = request.POST['customer_code']
        customer = Customer.objects.get(customer_code=customer_code)
        data = dict()
        if customer:
            customer.delete()
            data['message'] = "Customer Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        customers = list(Customer.objects.all().values())
        data['customers'] = customers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result




def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def room(request):
    return render(request, 'room.html')

def gallery(request):
    return render(request, 'gallery.html')

def roomtype(request):
    return render(request, 'roomtype.html')
def roomtype1(request):
    return render(request, 'roomtype1.html')
def roomtype2(request):
    return render(request, 'roomtype2.html')
def roomtype3(request):
    return render(request, 'roomtype3.html')

def regis(request):
    return render(request, 'regis.html')


@method_decorator(csrf_exempt, name='dispatch')
class login(View):
    template_name = 'login.html'
    
    def get(self, request):

        if 'user' in request.session:
            return redirect('home')
        else:
            return render(request, self.template_name)
    
    def post(self, request):
        mail = request.POST['email']
        pwd = request.POST['pwd']
        hash_pwd = md5(pwd.encode()).hexdigest()
        user_exists = Customer.objects.filter(email=mail, password=hash_pwd)
        print(mail)
        if user_exists.exists():
            request.session['user'] = user_exists.first().fname
        else:
            messages.warning(request, 'Wrong credentials')

        
        return render(request, 'home.html')


@method_decorator(csrf_exempt, name='dispatch')
class Customerlogin(View):
    template_name = 'login.html'
    def get(self, request):
        if 'user' in request.session:
            return redirect('home')
        else:
            return render(request, self.template_name)

    def post(self, request):

        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers
        
        return render(request, 'login.html', data)