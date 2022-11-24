"""lab4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from report import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='Index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('room', views.room, name='room'),
    path('gallery', views.gallery, name='gallery'),
    path('roomtype', views.roomtype, name='roomtype'),
    path('roomtype1', views.roomtype1, name='roomtype1'),
    path('roomtype2', views.roomtype2, name='roomtype2'),
    path('roomtype3', views.roomtype3, name='roomtype3'),
    path('regis', views.regis, name='regis'),
    path('login', views.login.as_view(), name='login'),
    #path('login', views.user_login, name='login'),

    #path('ReportListAllInvoices', views.ReportListAllInvoices),
    #path('ReportProductsSold',views.ReportProductsSold),
    #path('ReportListAllProducts',views.ReportListAllProducts),
    #path('ReportListAllPaymentMethod',views.ReportListAllPaymentMethod),
    #path('ReportListAllReceipts',views.ReportListAllReceipts),
    #path('ReportUnpaidInvoices',views.ReportUnpaidInvoices),
    
    #path('customer/list', views.CustomerList.as_view(), name='customer_list'), 
    #path('customer/get', views.customer), 
    #path('customer/get/<customer_code>', views.CustomerGet.as_view(), name='customer_get'), 
    path('account/save', views.AccountSave.as_view(), name='account_save'),   
    #path('customer/save2', views.CustomerSave2.as_view(), name='customer_save2'), 
    #path('customer/delete', views.CustomerDelete.as_view(), name='customer_delete'), 
    
]
