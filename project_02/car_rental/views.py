from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from datetime import datetime
#from .forms import *
from car_rental import models
from car_rental.models import Customer,Rental,Vehicle,Rate


# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def homepage(request):
    return render(request,'homepage.html')

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about_us.html')

def add_customer(request):
    if request.method=="POST":
        name = str(request.POST['cname'])
        phone = str(request.POST['cPhone'])
        ins = models.Customer(name=name,phone=phone)
        ins.save()
        messages.success(request, 'Customer has been successfully added.')
        #print (name,phone)
    return render(request,'add_customer.html')


def add_vehicle(request):
    if request.method=="POST":
        vehicleid = str(request.POST['vID'])
        description = str(request.POST['vDescription'])
        year = int(request.POST['vYear'])
        type = int(request.POST['vType'])
        category = int(request.POST['vCategory'])
        #print(vehicleid,description,year,type,category)
        ins = models.Vehicle(vehicleid=vehicleid,description=description,year=year,type=type,category=category)
        ins.save()

    return render(request,'add_vehicle.html')

def new_reservation(request):
    if request.method=="POST":
        rcID = int(request.POST['rcID'])
        rvID= str(request.POST['rvID'])
        rSd=str(request.POST['rSd'])
        rOd=str(request.POST['rOd'])
        rType=int(request.POST['rType'])
        rQty=int(request.POST['rQty'])
        rRd=str(request.POST['rRd'])
       
        
        # converting to date time format to perform calculations
        format_str='%m/%d/%Y'
        start=datetime.strptime(rSd,format_str).date()
        #order=datetime.strptime(rOd,format_str).date()
        returnDate=datetime.strptime(rRd,format_str).date()

        NofDay = returnDate-start
        #print(NofDay)
        NofDay=NofDay.days
        #print(NofDay)
    
        statement =("SELECT Weekly, Daily FROM RATE r, VEHICLE v WHERE v.VehicleID='"+rvID+"' AND v.Type=r.Type AND v.Category=r.Category")      
        
        with connection.cursor() as cursor:
            cursor.execute(statement)
            row = cursor.fetchone()
        
        totalamount=0
        #print(totalamount,NofDay)
        #print (row[0])
        #print(row[1])
        #calculating the cost of rental
        if rType == 7:
            #print(7)
            totalamount = int(NofDay)*float(row[0]) 
            
        elif rType==1:
            #print(1)
            totalamount= int(NofDay)*float(row[1])
        
        #check box
        paydate = None
        if request.POST.getlist("Paynow"):
            paydate=datetime.today()
            paydate=paydate.date()
            paydate=paydate.strftime('%m/%d/%Y')

       # _id for foreign key saving
        ins = models.Rental(custid_id=rcID, vehicleid_id=rvID,startdate=rSd,orderdate=rOd,rentaltype=rType,qty=rQty,returndate=rRd,totalamount=totalamount,paymentdate=paydate,returned=0)
        ins.save()

    return render(request,'new_reservation.html')

def book_reservation(request):
    return render(request,'book_reservation.html')

def book_reservation2(request):
    if request.method=="POST":
        rSd=str(request.POST['bSd'])
        rType=str(request.POST['bvType'])
        rRd=str(request.POST['bRd'])
        rCategory=str(request.POST['bvCategory'])
        #print(rSd,rType,rRd,rCategory)

        #finding available cars
        statement = ("SELECT v.VehicleID AS VIN, v.Description, v.Year FROM VEHICLE v LEFT JOIN RENTAL r ON v.VehicleID=r.VehicleID WHERE v.Type="+rType+" AND v.Category="+rCategory+"  AND v.VehicleID NOT IN (  SELECT r1.VehicleID FROM RENTAL r1 WHERE (str_to_Date(r1.StartDate, '%m/%d/%Y') BETWEEN	str_to_date('"+rSd + "','%m/%d/%Y') AND str_to_date('"+rRd+"','%m/%d/%Y'))	OR	(str_to_Date(r1.ReturnDate, '%m/%d/%Y') BETWEEN	str_to_date('"+rSd+"','%m/%d/%Y') AND str_to_date('"+rRd+"','%m/%d/%Y'))) GROUP BY v.VehicleID")
   
        with connection.cursor() as cursor:
            cursor.execute(statement)
            row=dictfetchall(cursor)
            udates={'StartDate':rSd,'ReturnDate':rRd}
            return render(request,'book_reservation2.html',context={'data':row,'uDate':udates})
 
def save_reservation(request):
    if request.method=="POST":
        rcID = int(request.POST['brcID'])
        rvID= str(request.POST['brvID'])
        rOd=str(request.POST['brOd'])
        rType=int(request.POST['brType'])
        rQty=int(request.POST['brQty'])
        rSd=str(request.POST['brSD'])
        rRd=str(request.POST['brRD'])

        # converting to date time format to perform calculations
        format_str='%m/%d/%Y'
        start=datetime.strptime(rSd,format_str).date()
        #order=datetime.strptime(rOd,format_str).date()
        returnDate=datetime.strptime(rRd,format_str).date()

        NofDay = returnDate-start
        #print(NofDay)
        NofDay=NofDay.days
        #print(NofDay)
    
        statement =("SELECT Weekly, Daily FROM RATE r, VEHICLE v WHERE v.VehicleID='"+rvID+"' AND v.Type=r.Type AND v.Category=r.Category")      
        
        with connection.cursor() as cursor:
            cursor.execute(statement)
            row = cursor.fetchone()
        
        totalamount=0
        if rType == 7:
            #print(7)
            totalamount = int(NofDay)*float(row[0]) 
            
        elif rType==1:
            #print(1)
            totalamount= int(NofDay)*float(row[1])

        paydate = None
        if request.POST.getlist("Paynow2"):
            paydate=datetime.today()
            paydate=paydate.date()
            paydate=paydate.strftime('%m/%d/%Y')

       # _id for foreign key saving
        ins = models.Rental(custid_id=rcID, vehicleid_id=rvID,startdate=rSd,orderdate=rOd,rentaltype=rType,qty=rQty,returndate=rRd,totalamount=totalamount,paymentdate=paydate,returned=0)
        ins.save()

    return render(request,'homepage.html')

def return_reservation2(request):
    return render(request,'return_reservation.html')

def return_reservation(request):
    if request.method=="POST":
        rVin=str(request.POST['rRVin'])
        rName=str(request.POST['rRName'])
        rDate=str(request.POST['rRDate'])

        statement =("SELECT CustID FROM CUSTOMER WHERE Name='"+rName+"'")
        with connection.cursor() as cursor:
            cursor.execute(statement)
            row = cursor.fetchone()
        
        #print(row[0])
        statement=("UPDATE RENTAL SET Rental.Returned=1 WHERE Rental.CustID="+str(row[0])+" AND Rental.VehicleID='"+rVin+"' AND str_to_date(Rental.ReturnDate,'%m/%d/%Y') = str_to_date('"+rDate+"','%m/%d/%Y')")
        with connection.cursor() as cursor:
            cursor.execute(statement)

        statement2=("SELECT PaymentDate FROM RENTAL WHERE Rental.CustID="+str(row[0])+" AND Rental.VehicleID='"+rVin+"' AND str_to_date(Rental.ReturnDate,'%m/%d/%Y') = str_to_date('"+rDate+"','%m/%d/%Y')")
        with connection.cursor() as cursor:
            cursor.execute(statement2)
            row1 = cursor.fetchone()
        
        if row1[0] is None: 
            paydate=datetime.today()
            paydate=paydate.date()
            paydate=paydate.strftime('%m/%d/%Y')
            #print(str(paydate))
                
            statement2=("UPDATE RENTAL SET Rental.PaymentDate='"+str(paydate)+"' WHERE Rental.CustID="+str(row[0])+" AND Rental.VehicleID='"+rVin+"' AND str_to_date(Rental.ReturnDate,'%m/%d/%Y') = str_to_date('"+rDate+"','%m/%d/%Y')")
            with connection.cursor() as cursor:
                cursor.execute(statement2)
          
        statement3=("SELECT OrderDate, StartDate,ReturnDate,TotalAmount, PaymentDate FROM RENTAL WHERE Rental.CustID="+str(row[0])+" AND Rental.VehicleID='"+rVin+"' AND str_to_date(Rental.ReturnDate,'%m/%d/%Y') = str_to_date('"+rDate+"','%m/%d/%Y')")
        with connection.cursor() as cursor:
            cursor.execute(statement3)
            row3=dictfetchall(cursor)
        
        print(row3)
        record={'Name':rName,'Id':row[0],'Vin':rVin}
        #print(record,row3)

    return render(request,'return_reservation2.html',context={'data':row3,'Info':record})
    

def view_customer(request):
    statement = ("SELECT c.CustID, c.Name, SUM(Case WHEN r.PaymentDate IS NULL THEN r.TotalAmount WHEN r.PaymentDate IS NOT NULL THEN 0  END) AS Balance FROM CUSTOMER c, Rental r WHERE r.custID=c.custID  GROUP BY c.Name")

    with connection.cursor() as cursor:
        cursor.execute(statement)
        row = dictfetchall(cursor)
        return render(request,'view_customer.html',{'data':row})

def view_customer2(request):
    if request.method=="POST":
        custName =request.POST['vcbName']
        custID=request.POST['vcbID']
        #print(len(custName), custId)
        #if no input is provided
        if (len(custName)==0) and (len(custID)==0):
            statement = ("SELECT c.CustID, c.Name, SUM(Case WHEN r.PaymentDate IS NULL THEN r.TotalAmount WHEN r.PaymentDate IS NOT NULL THEN 0  END) AS Balance FROM CUSTOMER c, Rental r WHERE r.custID=c.custID  GROUP BY c.Name")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request,'view_customer.html',{'data':row})

        #if only customer id is provided
        if (len(custName)==0) and (len(custID)!=0):
            statement = ("SELECT c.CustID, c.Name, SUM(Case WHEN r.PaymentDate IS NULL THEN r.TotalAmount WHEN r.PaymentDate IS NOT NULL THEN 0  END) AS Balance FROM CUSTOMER c, Rental r WHERE r.custID=c.custID AND r.custID="+custID+"  GROUP BY c.Name")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request,'view_customer.html',{'data':row})

        #if only customer name or part of name is provided
        if (len(custName)!=0) and (len(custID)==0):
            statement = ("SELECT c.CustID, c.Name, SUM(Case WHEN r.PaymentDate IS NULL THEN r.TotalAmount WHEN r.PaymentDate IS NOT NULL THEN 0 END) AS Balance FROM CUSTOMER c LEFT JOIN Rental r ON r.custID=c.custID  WHERE c.Name LIKE '%"+custName +"%'GROUP BY c.Name;")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request,'view_customer.html',{'data':row})
        
        #if both customer ID and name is entered
        if (len(custName)!=0) and (len(custID)!=0):
            statement = ("SELECT c.CustID, c.Name, SUM(Case WHEN r.PaymentDate IS NULL THEN r.TotalAmount WHEN r.PaymentDate IS NOT NULL THEN 0  END) AS Balance FROM CUSTOMER c, Rental r WHERE r.custID=c.custID AND r.custID="+custID+" AND c.Name='"+custName+"' GROUP BY c.Name")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request,'view_customer.html',{'data':row})

def view_vehicle(request):
    statement = ("SELECT v.VehicleID AS VIN, v.Description, r.Daily FROM Vehicle v Natural JOIN Rate r  GROUP BY v.VehicleID ORDER BY r.Daily;")
    with connection.cursor() as cursor:
        cursor.execute(statement)
        row = dictfetchall(cursor)
        return render(request, 'view_vehicle.html',{'data':row})

def view_vehicle2(request):
    if request.method=="POST":
        vehicleID = request.POST['vvVID']
        vehicleDescription = request.POST['vvDescription']
        #if nothing is provided
        if (len(vehicleID)==0) and (len(vehicleDescription)==0):
            statement = ("SELECT v.VehicleID AS VIN, v.Description, r.Daily FROM Vehicle v Natural JOIN Rate r  GROUP BY v.VehicleID ORDER BY r.Daily;")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request, 'view_vehicle.html',{'data':row})
        #if vehicle ID Is provided
        if (len(vehicleID)!=0) and (len(vehicleDescription)==0):
            statement = ("SELECT v.VehicleID AS VIN, v.Description, r.Daily FROM Vehicle v Natural JOIN Rate r WHERE v.VehicleID='"+ vehicleID +"' GROUP BY v.VehicleID ORDER BY r.Daily;")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request, 'view_vehicle.html',{'data':row})
        #if description is provided
        if (len(vehicleID)==0) and (len(vehicleDescription)!=0):
            statement = ("SELECT v.VehicleID AS VIN, v.Description, r.Daily FROM Vehicle v Natural JOIN Rate r WHERE v.Description LIKE '%"+ vehicleDescription +"%' GROUP BY v.VehicleID ORDER BY r.Daily;")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request, 'view_vehicle.html',{'data':row})
        #if both are provided
        if (len(vehicleID)!=0) and (len(vehicleDescription)!=0):
            statement = ("SELECT v.VehicleID AS VIN, v.Description, r.Daily FROM Vehicle v Natural JOIN Rate r WHERE v.Description='"+ vehicleDescription +"' AND v.VehicleID='"+ vehicleID +"' GROUP BY v.VehicleID ORDER BY r.Daily;")
            with connection.cursor() as cursor:
                cursor.execute(statement)
                row = dictfetchall(cursor)
                return render(request, 'view_vehicle.html',{'data':row})

