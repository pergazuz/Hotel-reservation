from django.db import models

# Create your models here.
class Data(models.Model):
    key = models.CharField(max_length=10,primary_key=True)
    value = models.CharField(max_length=100)



class Account(models.Model):
    customer_code = models.CharField(max_length=15,primary_key=True)
    customer_name = models.CharField(max_length=20)
    customer_lastname = models.CharField(max_length=20)
    birthday = models.DateField(null=True ,blank = True)
    address = models.CharField(max_length=200,null=True,blank= True)
    email = models.CharField(max_length=30,null=True,blank= True)
    phone_no = models.CharField(max_length=10,null=True,blank= True)
    password = models.CharField(max_length=100,null=True,blank= True)
    class Meta:
        db_table = "account"
        managed = False
    def __str__(self):
        return self.customer_code
    
class Promotion(models.Model):
    event = models.CharField(max_length=40,primary_key=True)
    discount = models.IntegerField(null=True)
    vat = models.IntegerField(null=True)
    amount_due = models.IntegerField(null=True)
    class Meta:
        db_table = "promotion"
        managed = False
    def __str__(self):
        return self.event

class Receipt(models.Model):
    receipt_no = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    customer_code = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='customer_code')
    payment_method = models.CharField(max_length=10, null=True, blank=True)
    payment_reference = models.CharField(max_length=10, null=True, blank=True)
    amount_due = models.IntegerField(null=True)
    class Meta:
        db_table = "receipt"
        managed = False
        
class Reserve(models.Model):
    reserve_no = models.CharField(max_length=20, primary_key=True)
    customer_code = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account', db_column='customer_code')
    room_no = models.CharField(max_length=20,null=True,blank= True)
    payment_method = models.CharField(max_length=20,null=True,blank= True)
    event = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='promotion', db_column='event', null=True)
    receipt_no = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='receipt', db_column='receipt_no')
    check_out_date = models.DateField(null=True ,blank = True)
    check_in_date = models.DateField(null=True ,blank = True)

    class Meta:
        db_table = "reserve"
        managed = False


class Room(models.Model):
    room_no = models.CharField(max_length=10, primary_key=True)
    room_type = models.CharField(max_length=20, null=True, blank=True)
    detail = models.CharField(max_length=20, null=True, blank=True)
    class Meta:
        db_table = "room"
        managed = False

# class ReserveLineItem(models.Model):
#     reserve_no = models.ForeignKey(Reserve, primary_key=True, on_delete=models.CASCADE, db_column='reserve_no')
#     reserve_item_no = models.IntegerField()
#     room_no = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room', db_column='room_no')
#     check_out_date = models.DateField(null=True ,blank = True)
#     check_in_date = models.DateField(null=True ,blank = True)
#     class Meta:
#         db_table = "reserve_line_item"
#         unique_together = (("reserve_no", "reserve_item_no"),)
#         managed = False
#     def __str__(self):
#         return '{"reserve_line_item":"%s","reserve_item_no":"%s","room_no":"%s","check_out_date":"%s","check_in_date":"%s"}' % (self.reserve_line_item, self.reserve_item_no, self.room_no, self.check_out_date, self.check_in_date)
        
class ReceiptLineItem(models.Model):
    receipt_no = models.ForeignKey(Receipt, primary_key=True, on_delete=models.CASCADE, db_column='receipt_no')
    item_receipt_no = models.IntegerField()
    room_no = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room', db_column='room_no')
    reserve_no = models.ForeignKey(Reserve, on_delete=models.CASCADE, related_name='reserve', db_column='reserve_no')
    payment_method = models.CharField(max_length=20)
    class Meta:
        db_table = "receipt_line_item"
        unique_together = (("receipt_no", "item_receipt_no"),)
        managed = False
    def __str__(self):
        return '{"receipt_no":"%s","item_receipt_no":"%s","room_no":"%s","reserve_no":"%s","payment_method":"%s"}' % (self.receipt_no, self.item_receipt_no, self.room_no, self.reserve_no, self.payment_method)

