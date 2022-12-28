from genericpath import exists
from sqlite3 import Date
from django.db import models
import datetime
from datetime import datetime,time,timedelta


from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserModel(models.Model):
    stu_id=models.AutoField(primary_key=True,editable=True)
    name= models.CharField(max_length=50,editable=True)
    first_name =models.CharField(max_length=50,editable=True)
    email = models.EmailField(unique=True,editable=True)
    password=models.CharField(max_length=50,editable=True)
    mobile = models.CharField(max_length=10,editable=True)
    city = models.CharField(max_length=50, null=True,editable=True)

    def __str__(self):
        return str(self.stu_id)


    
   
class Attendence(models.Model):
    id=models.AutoField(primary_key=True,editable=True)
    emp_id=models.ForeignKey(UserModel,on_delete=models.CASCADE,editable=True)
    name=models.CharField(max_length=50,editable=True)
    date=models.DateField(auto_now=False,unique=False,editable=True)
    In_Time=models.TimeField(auto_now=False,null=True,editable=True)
    Out_Time=models.TimeField(auto_now=False,null=True,editable=True)
    Work_type=models.CharField(max_length=50,null=True,editable=True)  
    Salary = models.CharField(max_length=50,editable=True)
    duration=models.DurationField(null=True,editable=True)
    total_second=models.FloatField(null=True,editable=True)
    sub_total=models.DecimalField(max_digits=300,decimal_places=2,null=True,editable=True)
    paid=models.BooleanField(default=False,editable=True)
    
    
    class Meta:
        unique_together = (('emp_id','date'),)

    def __str__(self):
        return str(self.In_Time.hour,self.In_Time.min)


    def __str__(self):
        return str(self.Out_Time.hour,self.Out_Time.min)

    def __str__(self):
        return str(self.emp_id)
    
    def __str__(self):
        return str(self.Salary)

    def __str__(self):
        return str(self.id)




    '''def hours_conversion(self):
        startdelta = datetime.timedelta(hours=self.In_Time.hour, minutes=self.In_Time.minute, seconds=self.In_Time.second)
        enddelta = datetime.timedelta(hours=self.Out_Time.hour, minutes=self.Out_Time.minute, seconds=self.Out_Time.second)
        return print((enddelta-startdelta).seconds/3600)'''


class Payments(models.Model):
    emp_id=models.ForeignKey(UserModel,on_delete=models.CASCADE,editable=True)
    attend_id=models.ForeignKey(Attendence,on_delete=models.CASCADE,editable=True)
    amount=models.DecimalField(max_digits=300,decimal_places=6,null=True,editable=True)
    receiver=models.CharField(max_length=50,null=True,editable=True)  
    completed_salary=models.DecimalField(max_digits=300,decimal_places=2,null=True,editable=True) 
    due_salary=models.DecimalField(max_digits=300,decimal_places=2,null=True,editable=True)   
    

    
    def __str__(self):
        return str(self.attend_id)

    def __str__(self):
        return str(self.emp_id)

class PayementStatus(models.Model):
    paid=models.BooleanField(default=False,editable=True)

    def __str__(self):
        return str(self.paid)