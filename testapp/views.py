import email
from django.shortcuts import render
from .forms import Form,Aform
from django.http import HttpResponseRedirect
from.models import PayementStatus, UserModel,Attendence,Payments
from datetime import datetime,time,timedelta
from itertools import chain
import math as m
from django.contrib import messages
from django.db.models.functions import ExtractHour,ExtractMinute
from django.db.models import DurationField, ExpressionWrapper, F,Sum,FloatField,DecimalField,IntegerField,DateTimeField
from .forms import SignUpForm,SignInForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from emp10 import settings 
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .token import generate_token




# Create your views here.
global sumsalary
sumsalary=0
def home(request):
    if request.user.is_authenticated:
        return render(request,'testapp/home.html')
    else:
        return HttpResponseRedirect("/signin/")

def user_add(request):
    if request.method=='POST':
        fm=Form(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Employee {} ,,, Added Successfully.'.format(fm.cleaned_data['first_name']))
            return HttpResponseRedirect('/add/')
    else:

        fm=Form()
    return render(request,"testapp/add.html",{'fm':fm})
    

def update(request,id):
    if request.method =='POST':
        pi=UserModel.objects.get(pk=id)
        fm=Form(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()   
            messages.success(request,"Your data is Successfully Updated")      
    else:
        pi=UserModel.objects.get(pk=id)
        fm=Form(instance=pi)
    return render(request,'testapp/update.html',{'fm':fm,'id':id})

def delete(request,id):
    if request.method=='GET':
        pi=UserModel.objects.get(pk=id)
        pi.delete() 
        return HttpResponseRedirect('/info/')

def user_info(request):
    stu=UserModel.objects.all()
    return render(request,'testapp/info.html',{'s':stu})



    #salary based

def user_attendence(request,id):

    initial_data={'emp_id':id,'name':UserModel.objects.get(pk=id).name}
   
    if request.method=='POST':
        fm=Aform(request.POST,initial=initial_data)
        if fm.is_valid():
            In_Time=fm.cleaned_data['In_Time']
            Out_Time=fm.cleaned_data['Out_Time']    
            if In_Time<=Out_Time:
                fm.save()
                t=PayementStatus(paid=False)
                t.save()
                

                url='/attend/{}'.format(id)
                return HttpResponseRedirect(url)
            else:
                messages.error(request,'Exist Time  cannot  be less than Entry Time.')
    else:

        fm=Aform(initial=initial_data)
    s=Attendence.objects.filter(emp_id=id).values()
    o=UserModel.objects.all()
    pi=UserModel.objects.get(pk=id)
    nm=pi.name
    return render(request,'testapp/attend.html',{'fm':fm,'nm':nm,'emp':id,'s':s,'o':o})

def update_attendence(request,id):
    if request.method =='POST':
        pi=Attendence.objects.get(pk=id)
        o=pi.emp_id
        fm=Aform(request.POST,instance=pi)
        if fm.is_valid():
            In_Time=fm.cleaned_data['In_Time']
            Out_Time=fm.cleaned_data['Out_Time']    
            if In_Time<=Out_Time:
                fm.save()   
                url='/attend/{}'.format(o)
                return HttpResponseRedirect(url)
            else:
                messages.error(request,'Exist Time  cannot  be less than Entry Time.') 
             
    else:
        pi=Attendence.objects.get(pk=id)
        o=pi.emp_id
        fm=Aform(instance=pi)
    s=Attendence.objects.filter(emp_id=o).values()
    return render(request,'testapp/attend.html',{'fm':fm,'id':id,'s':s})

def delete_attendence(request,id):
    if request.method=='GET':
        pi=Attendence.objects.get(pk=id)
        o=pi.emp_id
        pi.delete() 
        url='/attend/{}'.format(o)
        return HttpResponseRedirect(url)



def user_salary(request):
    
    '''p=Attendence.objects.all().values().annotate(duration=ExpressionWrapper(t.total_seconds(), output_field=DateTimeField()))
    print(p)
    l=dict()
    m=1'''
    '''for i in p:
        k=i.get('duration').total_seconds()/3600
        l[m]=k
        m+=1'''
    '''h=Attendence.objects.values_list('Out_Time','In_Time').update(duration=ExpressionWrapper(F('Out_Time') - F('In_Time'), output_field=DurationField()))
    print(h)
    l=dict()
    m=1
    for i in h:
        i=list(i)
        k=i[2].total_seconds()
        print(k)
        l[m]=k
        m+=1
    l1=dict()
    m=1
    for i in Attendence.objects.all().values_list('Salary'):
        for j in i:
            print(type(int(j)))
            print(type(l[m]))
            l1[m]=int(j)*l[m]/3600
            print('hi',l1[m])
        m+=1
    print(l1)'''
   
    #o=Attendence.objects.all().values().update_or_create(duration=ExpressionWrapper(F('Out_Time') - F('In_Time'), output_field=DurationField()),sub_total=ExpressionWrapper(F('Out_Time')* F('Salary') - F('In_Time') * F('Salary'),output_field=FloatField()))
    #S1=Attendence.objects.all().values_list('Salary')


    '''duration_expression = F('Out_Time') - F('In_Time')
    duration_wrapper = ExpressionWrapper(duration_expression,output_field=DurationField())
    duration_hours= ExtractHour(duration_wrapper)
    q=Attendence.objects.all().values().annotate(leave_duration=duration_hours)
    print('Hours',q)
    
    S=Attendence.objects.all().values().update(duration=F('Out_Time')- F('In_Time'))
    print(S)
    u=Attendence.objects.values_list('duration')
    print(u)
    for i in u:
        print(i)
        for j in i:
            print('prem',j)
   
    v=Attendence.objects.all()
    
    S1=Attendence.objects.all().values().annotate(ExpressionWrapper(sub_total=F('duration')*F('Salary'),output_field=FloatField()))
    print(S1)
    """ for i in o:
        for j in len(l1):
            if i.get("emp_id_id")==j+1:
                print('oyee',i)
                i.__setitem__=('salary',l1[j+1])"""
    #o[0]['total']=2500
    #print("hello",o[0])
    #d={'p':o,'k':l1}
    # <CombinedExpression: F(price) + Value(1)>
    #print("amma",o)'''
    
    s1=Attendence.objects.all().values().update(total_second=F("Out_Time")-F("In_Time"))
    s2=Attendence.objects.all().values().update(total_second=F("total_second")/3600000000.0)
    s=Attendence.objects.all().values().update(sub_total=F("Salary")*F("total_second"))
    s4=Attendence.objects.all().values().update(duration=F("Out_Time")-F("In_Time"))
    s3=Attendence.objects.all()
    '''s5=Attendence.objects.get(pk=id).emp_id.email
    s6=Attendence.objects.get(pk=id).emp_id.first_name
    s7=Attendence.objects.get(pk=id).sub_total
    rec=Payments.objects.filter(attend_id_id=Attendence.objects.get(pk=id).pk)
    total_salary=float(s7)
    remaining=0.0
    if not rec :
        o=Attendence.objects.get(pk=id).emp_id
        rec=Payments(attend_id_id=Attendence.objects.get(pk=id).pk,emp_id=o,receiver=s5,amount=total_salary,completed_salary=remaining,due_salary=total_salary)
        rec.save()'''

    '''t=PayementStatus(paid=False)
    t.save()'''
    '''rec=Payments.objects.all()
    print("kolol",rec)
    if not rec:
        print('kuch nhi h')
        d=PayementStatus.objects.all().values_list('paid')
    
    else:
        d=Payments.objects.all().values_list('paid')
    
    l=[]
    for i in d:
        l.append(i)'''
    return render(request,'testapp/salary.html',{'p':s3})




def user_present(request):
    today = datetime.now()
    try:
        if request.method=='POST':
            p=request.POST['empsearch']
            l=p.split('-')
            a=Attendence.objects.filter(date__year=l[0],date__month=l[1])
            b=a.values()
            nm=[]
            for i in b:
                c=i.get('emp_id_id')
                n=UserModel.objects.get(stu_id=c)
                nm.append(n)  
        else:
            a=Attendence.objects.filter(date__year=today.year,date__month=today.month) 
        nm=UserModel.objects.all()
        return render(request,'testapp/present.html',{'a':a,'nm':nm})
    except:
        a=Attendence.objects.filter(date__year=today.year,date__month=today.month) 
        nm=UserModel.objects.all()
        return render(request,'testapp/present.html',{'a':a,'nm':nm})

# login,logout

def user_signup(request):
    if request.method=='POST':
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            uname=fm.cleaned_data['username']
            pw=fm.cleaned_data['password1']
            fn=fm.cleaned_data['first_name']
            email=fm.cleaned_data['email']

            print('heloo')
            
             
            user=User.objects.get(username=uname)
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            email_subject="confirm your Email"
            massage2=render_to_string('testapp/confirm.html',
            {'name':user.first_name,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)}
            )

            fname=fn
            e=email
            p= email_subject
            t=e
            from_email=settings.EMAIL_HOST_USER
            msg=massage2
            send_mail(
                p,
                msg,
                from_email,
                [t],
                fail_silently=True,
                )
                    # messages.success(request,"Logged in successfully.")
            #messages.success(request,"Account has been Created Successfully...")
            
           
            messages.success(request,"Account has been Created Successfully...,Check your email to login")
            return HttpResponseRedirect('/')
    else:
        fm=SignUpForm()
    return render(request,'testapp/signup.html',{'fm':fm})

def user_signin(request):
    
    
    if not request.user.is_authenticated:
        if request.method=="POST": 
            fm=SignInForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                password1=fm.cleaned_data['password']
                user=authenticate(username=uname,password=password1)
                if user is not None:
                    login(request,user)
                    fname=request.user.first_name
                    e=request.user.email
                    p= "Hello "+ fname
                    t=e
                    from_email=settings.EMAIL_HOST_USER
                    msg="Congratulations,You are Logged in successfully."
                    send_mail(
                            p,
                            msg,
                            from_email,
                            [t],
                            fail_silently=True,
                            )
                    return render(request,"testapp/home.html")
        else:
            fm=SignInForm()
        return render(request,'testapp/signin.html',{'fm':fm})
    else:
        return HttpResponseRedirect("/home/")

    
    

    

def user_signout(request):
    if request.user.is_authenticated:
        logout(request)
        #return render(request,'testapp/home.html')
    
    return HttpResponseRedirect("/signin/")

def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
        context = {'uidb64':uidb64, 'token':token}
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and generate_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        return render(request,'testapp/home.html',context)
    else:
        return HttpResponseRedirect('/e/')

def err(request):
    return render(request,'testapp/e.html')

def payment(request,id,f=0):
    '''s1=Attendence.objects.all().values().update(total_second=F("Out_Time")-F("In_Time"))
    s2=Attendence.objects.all().values().update(total_second=F("total_second")/3600000000.0)
    s=Attendence.objects.all().values().update(sub_total=F("Salary")*F("total_second"))
    s4=Attendence.objects.all().values().update(duration=F("Out_Time")-F("In_Time"))
    s3=Attendence.objects.get(pk=id).sub_total'''
    s5=Attendence.objects.get(pk=id).emp_id.email
    s6=Attendence.objects.get(pk=id).emp_id.first_name
    s7=Attendence.objects.get(pk=id).sub_total
    rec=Payments.objects.filter(attend_id_id=Attendence.objects.get(pk=id).pk)
    total_salary=float(s7)
    remaining=0.0
    if not rec :
        o=Attendence.objects.get(pk=id).emp_id
        rec=Payments(attend_id_id=Attendence.objects.get(pk=id).pk,emp_id=o,receiver=s5,amount=total_salary,completed_salary=remaining,due_salary=total_salary)
        rec.save()
    r=Payments.objects.filter(attend_id=id).values_list('completed_salary')
    for i in r[0]:
        t=i
        print(t)
    if f==1 and t==0.00:
        Payments.objects.filter(attend_id=id).values_list('completed_salary').update(completed_salary=F('due_salary'))
        Payments.objects.filter(attend_id=id).values_list('due_salary').update(due_salary=F('completed_salary')*0.0)
        Attendence.objects.filter(pk=id).values_list('paid').update(paid=True)
        print(Payments.objects.filter(attend_id=id).values_list('due_salary'))   
    #Payments.objects.filter(attend_id=id).values_list('completed_salary').update(completed_salary=F('due_salary'))'''
    #messages.error(request,'bhai due amount dekh kr daal')
   
    #if f==0 and rec.completed_salary==0.00:


    '''receiver_obj=Payments.objects.get(receiver=r)
        p=Payments.objects.all()
        receiver_obj.amount=float(sum)
        receiver_obj.completed_salary=float(a)
        receiver_obj.due_salary-=float(a)
        print(receiver_obj)
        receiver_obj.save()'''
    user1=Payments.objects.filter(attend_id=id).values_list('completed_salary','due_salary')
    n=Payments.objects.filter(attend_id=id).values_list('due_salary')
    l=n[0][0]
    return render(request,'testapp/payment.html',{'e':s5,'h':s6,'l':l,'b':user1,'k':id,'a':remaining})

def payment_done(request,id): 

    '''print(f)
    print(Payments.objects.filter(attend_id=ids).values_list('completed_salary'))
    print(Payments.objects.filter(attend_id=ids).values_list('due_salary'))
    r=Payments.objects.filter(attend_id=ids).values_list('completed_salary')
    for i in r[0]:
        t=i
        print(t)
    if f==1 and t==0.00:
        Payments.objects.filter(attend_id=ids).values_list('completed_salary').update(completed_salary=F('due_salary'))
        Payments.objects.filter(attend_id=ids).values_list('due_salary').update(due_salary=F('completed_salary')*0.0)
        Payments.objects.filter(attend_id=ids).values_list('paid').update(paid=True)
        print(Payments.objects.filter(attend_id=ids).values_list('due_salary'))'''
    return render(request,'testapp/paymentdone.html',{'id':id})
    
    '''if rec :
        if rec.completed_salary==0.00 and rec.due_salary!=0.00:
            rec.completed_salary=rec.due_salary
            rec.due_salary=0.00
            rec.save()
        elif rec.completed_salary!=0.00 and rec.due_salary==0.00:
            url='/paymentdone/{}'.format(Payments.objects.get(pk=ids))
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect('/payment/')
     else :
        url='/payment/{}'.format(Payments.objects.get(pk=ids))
        return HttpResponseRedirect(url)'''
    
    