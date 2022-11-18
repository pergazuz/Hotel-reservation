from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import View
from django.db import connection
from report.models import *

from django.db import connection

# Create your views here.
from django.http import JsonResponse
def index(request):
    return render(request, 'home.html')


def ReportListAllProducts(request):

    dataReport = dict()
    data = list(Product.objects.all().values())
    columns = ("Code", "Name", "Units", "Product Type")
    dataReport['column_name'] = columns
    dataReport['data'] = data
    
    return render(request, 'report_list_all_products.html', dataReport)

def ReportListAllInvoices(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT i.invoice_no as "Invoice No", i.date as "Date" '
                             ' , i.customer_code as "Customer Code", c.name as "Customer Name" '
                             ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                             ' , ili.product_code as "Product Code", p.name as "Product Name" '
                             ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.product_total as "Extended Price" '
                             ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                             '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                             '  JOIN product p ON ili.product_code = p.code '
                             ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_list_all_invoices.html', dataReport)

def ReportProductsSold(request):

    cursor = connection.cursor()
    cursor.execute ('SELECT ili.product_code as "Product Code", p.name as "Product Name" '
                    ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.product_total) as "Total Value Sold" '
                    ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                    '   JOIN product p ON ili.product_code = p.code '
                    ' GROUP BY p.code, ili.product_code, p.name '
                    ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)
    print(columns)
    return render(request, 'report_products_sold.html', dataReport)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result


def ReportListAllReceipts(request):

    cursor = connection.cursor()

    cursor.execute ('SELECT r.receipt_no as "Receipt No", r.date as "Date", r.customer_code as "Customer Code" ' 
                            ' , c.name as "Customer Name", p.description as "Payment Name" ' 
                            ' , r.total_received as "Total Received", r.payment_reference as "Payment Reference", r.remarks as "Remarks" ' 
                            ' FROM receipt as r ' 
                            ' JOIN customer as c ON c.customer_code = r.customer_code '
                            ' JOIN payment_method as p ON p.payment_method = r.payment_method '
                            ' ')
            

    dataReport1 = dict()
    columns1 = [col[0] for col in cursor.description]
    data1 = cursor.fetchall()
        
    cursor.execute ('SELECT i.invoice_no as "Invoice No", i.date as "Invoice Date", i.amount_due as "Invoice Full Amount", rli.amount_paid_here as "Amount Paid Here", r.receipt_no '
                            '  FROM invoice as i '
                            '  JOIN receipt_line_item as rli '
                            ' ON rli.invoice_no = i.invoice_no '
                            ' JOIN receipt as r '
                            ' ON r.receipt_no = rli.receipt_no '
                            ' ')
            
    columns2 = [col[0] for col in cursor.description]
    data2 = cursor.fetchall()
            

    dataReport1['column_name1'] = columns1
    dataReport1['column_name2'] = columns2

    dataReport1['data1'] = CursorToDict(data1,columns1)
    dataReport1['data2'] = CursorToDict(data2,columns2)

    #for loop to show lineitem
    e, li = 0, []
    for i in dataReport1['data1']:
        j = str(dataReport1['data1'][e]['receipt_no'])
        e += 1
        li.append(j)


    dataReport1['Receipt_num'] = li
    dataReport1['column_name2'].remove("receipt_no")

    return render(request, 'report_list_all_receipts.html', dataReport1)


def ReportListAllPaymentMethod(request):

    dataReport = dict()
    data = list(PaymentMethod.objects.all().values())
    columns = ("Payment Method", "Description")
    dataReport['column_name'] = columns
    dataReport['data'] = data

    return render(request, 'report_list_all_payment_method.html', dataReport)

def ReportUnpaidInvoices(request):
    cursor = connection.cursor()

    
    cursor.execute ('SELECT i.invoice_no as "Invoice No", i.date as "Date", i.customer_code as "Customer Code" '
                               ' , c.name as "Customer Name", '
                               ' i.amount_due as "Amount Due", i.amount_due - ( '
                               ' SELECT SUM(amount_paid_here) FROM receipt_line_item WHERE invoice_no = i.invoice_no) as "Amount Received" '
                               ' FROM invoice as i '
                               ' JOIN customer as c '
                               ' ON i.customer_code = c.customer_code '
                               ' WHERE i.amount_due - (SELECT SUM(amount_paid_here) FROM receipt_line_item WHERE invoice_no = i.invoice_no) IS NOT NULL ')

    dataReport = dict()
    columns1 = [col[0] for col in cursor.description]
    data1 = cursor.fetchall()

    cursor.execute('SELECT COUNT(i.invoice_no) as "Number of Invoices Not Paid",SUM(i.amount_due - (SELECT SUM(amount_paid_here) '
                              '  FROM receipt_line_item WHERE invoice_no = i.invoice_no)) as "Total Invoice Amount Not Paid" FROM invoice as i '
                              '  WHERE i.amount_due - (SELECT SUM(amount_paid_here) FROM receipt_line_item WHERE invoice_no = i.invoice_no) IS NOT NULL')


    columns2 = [col[0] for col in cursor.description]
    data2 = cursor.fetchall()


    dataReport['column_name1'] = columns1
    dataReport['column_name2'] = columns2

    dataReport['data1'] = CursorToDict(data1,columns1)
    dataReport['data2'] = CursorToDict(data2,columns2)
    

    return render(request, 'report_unpaid_invoices.html', dataReport)

def about(request):
    return render(request, 'about.html')

def home(request):
    return render(request, 'home.html')