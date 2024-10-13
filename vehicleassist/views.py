from django.db.models import Q, Max, Sum
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta, time
import random

def index(request):
    try:
        error = ""
        if request.method == "POST":
            fname = request.POST['firstName']
            lname = request.POST['lastName']
            email = request.POST['emailid']
            bookingNo = str(random.randint(10000000, 99999999))
            PhoneNumber = request.POST['PhoneNumber']
            PickupLoc = request.POST['PickupLoc']
            Destination = request.POST['Destination']
            PickupDate = request.POST['PickupDate']
            PickupTime = request.POST['PickupTime']
            try:
                user = User.objects.create_user(username=email, first_name=fname, last_name=lname)
                Book.objects.create(user=user, BookingNumber=bookingNo, PhoneNumber=PhoneNumber, PickupLoc=PickupLoc,
                                    Destination=Destination,
                                    PickupDate=PickupDate, PickupTime=PickupTime)
                error = "no"
            except:
                error = "yes"
    except:
        if request.method == 'POST':
            u = request.POST['username']
            p = request.POST['password']
            user = authenticate(username=u, password=p)
            try:
                if user.is_staff:
                    login(request, user)
                    error1 = "no"
                else:
                    error1 = "yes"
            except:
                error1 = "yes"
    return render(request, 'index.html', locals())


def dashboard(request):
    totalnewreq = Book.objects.filter(Status__isnull=True).count()
    totalapprovedreq = Book.objects.filter(Status='Approved').count()
    totalrejectreq = Book.objects.filter(Status='Rejected').count()
    totalonthewayreq = Book.objects.filter(Status='On The Way').count()
    totalcompletereq = Book.objects.filter(Status='Completed').count()
    totaldriver = Driver.objects.all().count()
    return render(request, 'admin/dashboard.html', locals())

def addDriver(request):
    driverid = 1001 if Driver.objects.count() == 0 else Driver.objects.aggregate(max=Max('DriverID'))["max"] + 1
    error = ""
    if request.method == "POST":
        fname = request.POST['firstName']
        mob = request.POST['MobileNumber']
        email = request.POST['emailid']
        address = request.POST['Address']
        pwd = request.POST['password']
        try:
            user = User.objects.create_user(username=email, password=pwd, first_name=fname)
            Driver.objects.create(user=user, DriverID=driverid, MobileNumber=mob, Address=address)
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/addDriver.html', locals())

def manageDriver(request):
    driver = Driver.objects.all()
    return render(request, 'admin/manageDriver.html', locals())

def editDriver(request, pid):
    driver = Driver.objects.get(id=pid)
    error = ""
    if request.method == "POST":
        fname = request.POST['firstName']
        mob = request.POST['MobileNumber']
        address = request.POST['Address']

        driver.user.first_name = fname
        driver.MobileNumber = mob
        driver.Address = address

        try:
            driver.save()
            driver.user.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/editDriver.html', locals())

def deleteDriver(request, pid):
    User.objects.get(id=pid).delete()
    return redirect('admin/manageDriver')


def newRequest(request):
    book = Book.objects.filter(Status__isnull=True)
    return render(request, 'admin/newRequest.html', locals())


def approvedRequest(request):
    book = Book.objects.filter(Status='Approved')
    return render(request, 'admin/approvedRequest.html', locals())


def cancelRequest(request):
    book = Book.objects.filter(Status='Rejected')
    return render(request, 'admin/cancelRequest.html', locals())


def allRequest(request):
    book = Book.objects.all()
    return render(request, 'admin/allRequest.html', locals())


def viewRequestDetails(request, pid):
    book = Book.objects.get(id=pid)
    report1 = Tracking.objects.filter(book=book)
    bookid = book.id
    driver = Driver.objects.all()

    reportcount = Tracking.objects.filter(book=book).count()
    if request.method == "POST":
        cid = request.POST['AssignTo']
        driverid = Driver.objects.get(id=cid)

        status = request.POST['Status']
        remark = request.POST['Remark']

        try:
            reporttracking = Tracking.objects.create(book=book, Remark=remark, Status=status)
            book.Remark = remark
            book.Status = status
            book.AssignTo = driverid
            book.UpdationDate = date.today()
            book.save()
            error1 = "no"
        except:
            error1 = "yes"
    return render(request, 'admin/viewRequestDetails.html', locals())


def deleteRequest(request, pid):
    User.objects.get(id=pid).delete()
    return redirect('admin/allRequest')


def onethewayDriver(request):
    book = Book.objects.filter(Status='On The Way')
    return render(request, 'admin/onethewayDriver.html', locals())


def taskComplete(request):
    book = Book.objects.filter(Status='Completed')
    return render(request, 'admin/taskComplete.html', locals())


def betweendateReport(request):
    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']
        book = Book.objects.filter(Q(DateofRequest__gte=fd) & Q(DateofRequest__lte=td))
        return render(request, 'admin/betweendateReportDtls.html', locals())
    return render(request, 'admin/betweendateReport.html')

def search(request):
    sd = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
        try:
            user = [i.id for i in User.objects.filter(Q(first_name__icontains=sd) | Q(last_name__icontains=sd))]
            book = Book.objects.filter(Q(user__in=user) | Q(BookingNumber=sd) | Q(PhoneNumber=sd))
        except:
            book=""
    return render(request, 'admin/search.html', locals())


def changePassword(request):
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'admin/changePassword.html', locals())

    # ================================  Driver  ================================


def driverlogin(request):
    error = ""
    if request.method == 'POST':
        email = request.POST['emailid']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'driverlogin.html', locals())


def ddashboard(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    user = request.user
    driver = Driver.objects.get(user=user)
    totaldnewreq = Book.objects.filter(AssignTo=driver, Status='Approved').count()
    totaldontheway = Book.objects.filter(AssignTo=driver, Status='On The Way').count()
    totalcomplete = Book.objects.filter(AssignTo=driver, Status='Completed').count()
    return render(request, 'driver/ddashboard.html', locals())

def profile(request):
    user = User.objects.get(id=request.user.id)
    driver = Driver.objects.get(user=user)

    if request.method == "POST":
        fname = request.POST['firstName']
        mob = request.POST['MobileNumber']
        address = request.POST['Address']

        driver.user.first_name = fname
        driver.MobileNumber = mob
        driver.Address = address

        try:
            driver.save()
            driver.user.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'driver/profile.html', locals())


def newsRequest(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    user = request.user
    driver = Driver.objects.get(user=user)
    book = Book.objects.filter(AssignTo=driver, Status='Approved')
    return render(request, 'driver/newsRequest.html', locals())


def onthewayRequest(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    user = request.user
    driver = Driver.objects.get(user=user)
    book = Book.objects.filter(AssignTo=driver, Status='On The Way')
    return render(request, 'driver/onthewayRequest.html', locals())


def completedRequest(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    user = request.user
    driver = Driver.objects.get(user=user)
    book = Book.objects.filter(AssignTo=driver, Status='Completed')
    return render(request, 'driver/completedRequest.html', locals())


def totalRequest(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    user = request.user
    driver = Driver.objects.get(user=user)
    book = Book.objects.filter(AssignTo=driver)
    return render(request, 'driver/totalRequest.html', locals())


def dviewRequestDetails(request, pid):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    user = request.user
    driver = Driver.objects.get(user=user)
    book = Book.objects.get(AssignTo=driver, id=pid)
    report1 = Tracking.objects.filter(book=book)

    reportcount = Tracking.objects.filter(book=book).count()
    if request.method == "POST":
        status = request.POST['Status']
        remark = request.POST['Remark']

        try:
            reporttracking = Tracking.objects.create(book=book, Remark=remark, Status=status)
            book.Remark = remark
            book.Status = status
            book.UpdationDate = date.today()
            book.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'driver/dviewRequestDetails.html', locals())


def dsearch(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    sd = None

    if request.method == 'POST':
        sd = request.POST['searchdata']
        user1 = request.user
        driver = Driver.objects.get(user=user1)
        try:
            user = [i.id for i in User.objects.filter(Q(first_name__icontains=sd) | Q(last_name__icontains=sd))]
            book1 = Book.objects.filter(Q(user__in=user) | Q(BookingNumber=sd) | Q(PhoneNumber=sd), AssignTo=driver)
        except:
            book1=""
    return render(request, 'driver/dsearch.html',locals())


def dbetweendateReport(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']
        user = request.user
        driver = Driver.objects.get(user=user)
        book = Book.objects.filter(Q(DateofRequest__gte=fd) & Q(DateofRequest__lte=td), AssignTo=driver)
        return render(request, 'driver/dbetweenReportDtls.html', locals())

    return render(request, 'driver/dbetweendateReport.html')


def dchangePassword(request):
    if not request.user.is_authenticated:
        return redirect('driverlogin')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'driver/dchangePassword.html', locals())

def Logout(request):
    logout(request)
    return redirect('index')
