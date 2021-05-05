from django.urls import path, include
from . import views

urlpatterns=[
    path('',views.homepage, name='homepage'),
    path('index',views.index,name='index'),
    path('about',views.about,name='about'),
    path('add_customer', views.add_customer, name="add_customer"),
    path('add_vehicle',views.add_vehicle,name="add_vehicle"),
    path('new_reservation',views.new_reservation, name="new_reservation"),
    path('book_reservation',views.book_reservation,name="book_reservation"),
    path('book_reservation2',views.book_reservation2,name="book_reservation2"),
    path('save_reservation',views.save_reservation,name="save_reservation"),
    path('return_reservation2',views.return_reservation2,name="return_reservation2"),
    path('return_reservation',views.return_reservation,name="return_reservation"),
    path('view_customer',views.view_customer,name="view_customer"),
    path('view_customer2',views.view_customer2,name="view_customer2"),
    path('view_vehicle',views.view_vehicle,name="view_vehicle"),
    path('view_vehicle2',views.view_vehicle2,name="view_vehicle2"),

]