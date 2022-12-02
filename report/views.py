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
from django.contrib.auth import authenticate
from django.db import models

def index(request):
    return render(request, 'home.html')


def account(request):
    customer_code = request.GET.get('customer_code', '')
    accounts = list(Account.objects.filter(customer_code=customer_code).values())
    data = dict()
    data['accounts'] = accounts
    
    return render(request, 'login.html', data)

# class ProductList(View):
#     def get(self, request):
#         products = list(Product.objects.all().values())
#         data = dict()
#         data['products'] = products

#         return JsonResponse(data)

# class CustomerList(View):
#     def get(self, request):
#         customers = list(Customer.objects.all().values())
#         data = dict()
#         data['customers'] = customers

#         return JsonResponse(data)

# class CustomerGet(View):
#     def get(self, request, customer_code):
#         customers = list(Customer.objects.filter(customer_code=customer_code).values())
#         data = dict()
#         data['customers'] = customers

#         return JsonResponse(data)        

@method_decorator(csrf_exempt, name='dispatch')
class AccountSave(View):
    def post(self, request):
        form = AccountForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        accounts = list(Account.objects.all().values())
        data = dict()
        data['accounts'] = accounts
        
        return render(request, 'login.html', data)

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


# @method_decorator(csrf_exempt, name='dispatch')
# class CustomerDelete(View):
#     def post(self, request):

#         customer_code = request.POST['customer_code']
#         customer = Customer.objects.get(customer_code=customer_code)
#         data = dict()
#         if customer:
#             customer.delete()
#             data['message'] = "Customer Deleted!"
#         else:
#             data['message'] = "Error!"
#             return JsonResponse(data)

#         customers = list(Customer.objects.all().values())
#         data['customers'] = customers

#         return JsonResponse(data)
#         #return render(request, 'forms_customer.html', data)





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

def home(request):
    return render(request, 'home.html')
def jogin(request):
    return render(request,'jogin.html')

#@method_decorator(csrf_exempt, name='dispatch')
#class login(View):
    template_name = 'login.html'
    def get(self, request):
        if 'user' in request.session:
            return redirect('home')
        else:
            return render(request, self.template_name)

    def post(self, request):
        mail = request.POST['email']
        pwd = request.POST['password']
        hash_pwd = md5(pwd.encode()).hexdigest()
        user_exists = Account.objects.filter(email=mail, password=hash_pwd)
        if user_exists.exists():
            request.session['user'] = user_exists.email
        else:
            messages.warning(request, 'Wrong credentials')
            return redirect('regis')
def login(request):
    if request.method =='POST':
        email1=request.POST['email']
        password1=request.POST['password']
        x = authenticate(email=email1,password=password1)
        #print(x)
        #print(email)
        #print(password)
        try:
            if Account.objects.all().get(email=email1,password=password1):         
                messages.success(request,"เข้าสู่ระบบสำเร็จ")
                return redirect('jogin')
        except:
            pass
    response = render(request,'login.html')
    return HttpResponse(response)


