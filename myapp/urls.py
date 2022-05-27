from django.urls import path
from . import views
from django.contrib import admin

urlpatterns=[
    path('home/',views.home,name='home'),
    path('',views.home,name='home'),
    path('loginProf/',views.loginProf,name='loginProf'),
    path('signout/',views.signout,name='signout'),
    path('student/',views.student,name='student'),
    path('secureLog/',views.secureLog,name='secureLog'),
    path('scan/',views.scan,name='scan'),
    path('reset/',views.scan,name='reset'),
    path('manual/',views.manual,name='manual'),
    path('secureLog/edit/<str:id>',views.edit,name='edit'),
]
