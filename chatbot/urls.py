from django.contrib import admin
from django.urls import path
from chatbot import views

urlpatterns = [
    path('',views.index,name='index'),
    path('admin_index/',views.admin_index,name='admin_index'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('admin_aboutus/',views.admin_aboutus,name='admin_aboutus'),
    path('dept/',views.dept,name='dept'),
    path('raised/',views.raised,name='raised'),
    path('login/',views.login,name='login'),
    path("answer/", views.answer_it, name="answer_it"),
    path('gov/',views.gov,name='gov'),
    path('gov_data/<depth>',views.gov_data,name='gov_data')
]