from django.contrib import admin

from .models import UserModel,Attendence,Payments,PayementStatus

# Register your models here.
@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display=('stu_id','name','first_name','email','password','mobile','city')

@admin.register(Attendence)
class AttendenceAdmin(admin.ModelAdmin):
    list_display=('id','name','emp_id','date','In_Time','Out_Time','Work_type','Salary','duration','sub_total','paid')
    search_fields=('date','Work_type')

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display=('id','emp_id','attend_id','receiver','amount','completed_salary','due_salary')
    
@admin.register(PayementStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display=('id','paid')   