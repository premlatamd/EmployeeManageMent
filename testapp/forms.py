from dataclasses import fields
from .models import Attendence,UserModel
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username=forms.CharField(error_messages = {'required':"Please Enter Unique userName"} ,label='Username',widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(error_messages = {'required':"Please Enter First Name"},label='First Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','first_name','email','password1','password2']
    
class SignInForm(AuthenticationForm):
    username=forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control'}),error_messages={'required':'Please Enter existing Username'})
    password=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={'required':'Please Enter correct password'})
    class Meta:
        model:User
        fields=['username','password']


class Form(forms.ModelForm):
    mobile = forms.CharField(error_messages = {'required':"Please Enter  Your Mobile Number"} ,label='Mobile Number',widget=forms.NumberInput(attrs={'class':'form-control'}),max_length=10, min_length=10)
    class Meta:
        model=UserModel
        fields=['name','first_name','email','password','mobile','city']
        


        widgets={
        'name':forms.TextInput(attrs={'class':'form-control'}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        'password':forms.PasswordInput(render_value=True,attrs={'class':'form-control'}),
        'mobile':forms.NumberInput(attrs={'class':' form-control'}),
        'city':forms.TextInput(attrs={'class':' form-control'})
        }

        

class Aform(forms.ModelForm):
    WORK_CHOICES=[('Labour','Labour'),('Mason','Mason'),('Constructor','constructor')]
    SALARY=[('200',200),('400',400),('1000',1000),]
    #('constructor', 'Constructor')
    
    
    Work_type=forms.CharField(label='Work Type:',widget=forms.Select(choices=WORK_CHOICES,attrs={'class':'form-control'}))
    Salary=forms.IntegerField(label='Salary:',widget=forms.Select(choices=SALARY,attrs={'class':'form-control'}))
    class Meta:
        model=Attendence
        fields=['name','emp_id','date','In_Time','Out_Time','Work_type','Salary']

        widgets={
        'emp_id':forms.NumberInput(attrs={'class':'form-control',"readonly":"True"}),
        'name':forms.TextInput(attrs={'class':'form-control',"readonly":"True"}),
        'date':forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control','type': 'date'}),
        'In_Time':forms.TimeInput(format=('%H:%M:%S'),attrs={'class':'form-control','type':'time'}),
        'Out_Time':forms.TimeInput(format=('%H:%M:%S'),attrs={'class':'form-control','type':'time'}),
        #'Work_type':forms.TextInput(attrs={'class':'form-control'}),
        #'Salary':forms.NumberInput()
        }
        error_messages={
            'date':{'required':'Please Enter Date'},
            'In_Time':{'required':'Please Enter Entry Time'},
            'Out_Time':{'required':'Please Enter Exist Time'},
            'Work_type':{'required':'Please Enter Working Field'}
            
        }

