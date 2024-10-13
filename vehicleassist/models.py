from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    DriverID = models.IntegerField(null=True)
    MobileNumber = models.CharField(max_length=15, null=True)
    Address = models.CharField(max_length=150, null=True)
    JoiningDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    BookingNumber = models.CharField(max_length=150, null=True)
    PhoneNumber = models.CharField(max_length=15, null=True)
    PickupLoc = models.CharField(max_length=150, null=True)
    Destination = models.CharField(max_length=200, null=True)
    PickupDate = models.DateField(null=True)
    PickupTime = models.TimeField(null=True)
    DateofRequest = models.DateTimeField(auto_now_add=True)
    Remark = models.CharField(max_length=250, null=True)
    Status = models.CharField(max_length=150, null=True)
    AssignTo = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    UpdationDate = models.DateField(null=True)

    def __str__(self):
        return self.user.first_name



class Tracking(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    Remark = models.CharField(max_length=250, null=True)
    Status = models.CharField(max_length=150, null=True)
    UpdationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Remark
