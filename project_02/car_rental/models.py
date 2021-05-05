from django.forms import ModelForm
from django.db import models


class Customer(models.Model):
    custid = models.AutoField(db_column='CustID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class Rate(models.Model):
    type = models.IntegerField(db_column='Type', primary_key=True)  # Field name made lowercase.
    category = models.IntegerField(db_column='Category')  # Field name made lowercase.
    weekly = models.FloatField(db_column='Weekly', blank=True, null=True)  # Field name made lowercase.
    daily = models.FloatField(db_column='Daily', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rate'
        unique_together = (('type', 'category'),)





class Vehicle(models.Model):
    vehicleid = models.CharField(db_column='VehicleID', primary_key=True, max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=40, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    category = models.IntegerField(db_column='Category', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vehicle'


class Rental(models.Model):
    custid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustID')  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    startdate = models.CharField(db_column='StartDate', max_length=11, blank=True, null=True)  # Field name made lowercase.
    orderdate = models.CharField(db_column='OrderDate', max_length=11, blank=True, null=True)  # Field name made lowercase.
    rentaltype = models.IntegerField(db_column='RentalType')  # Field name made lowercase.
    qty = models.IntegerField(db_column='Qty', blank=True, null=True)  # Field name made lowercase.
    returndate = models.CharField(db_column='ReturnDate', max_length=11, blank=True, null=True)  # Field name made lowercase.
    totalamount = models.FloatField(db_column='TotalAmount', blank=True, null=True)  # Field name made lowercase.
    paymentdate = models.CharField(db_column='PaymentDate', max_length=11, blank=True, null=True)  # Field name made lowercase.
    returned = models.IntegerField(db_column='Returned', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'rental'