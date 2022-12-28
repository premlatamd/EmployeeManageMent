"""emp10 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home,name='home'),
    path('add/',views.user_add,name='add'),
    path('info/',views.user_info,name='info'),
    path('attend/<int:id>/',views.user_attendence,name='attendence'),
    path('salary/',views.user_salary,name='salary'),
    path('present/',views.user_present,name='present'),
    path('<int:id>/', views.update, name='updatedata'),
    path('update/<int:id>/', views.update_attendence, name='update_attend'),
    path('delete/<int:id>/', views.delete, name='deletedata'),
    path('delete_attend/<int:id>/', views.delete_attendence, name='delete_attend'),
    path('signin/', views.user_signin,name='signin'),
    path('payment/<int:id>/<int:f>', views.payment,name='payment'),
    path('', views.user_signup,name='signup'),
    path('signout/', views.user_signout,name='signout'),
    path('e/', views.err,name='e'),
    path('paymentdone/<int:id>', views.payment_done,name='paymentdone'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),
]
