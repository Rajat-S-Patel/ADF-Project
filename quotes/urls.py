from django import contrib
from django.urls import path,include
from . import views

urlpatterns = [
  path('',views.main,name='main'),
  #path('login',views.login,name='login'),
  path('accounts/',include('django.contrib.auth.urls')),
  path('home',views.home,name='home'),
   path('home/<ticker>',views.home,name='home_ticker'),
  path('register',views.register,name='register'),
  path('about',views.about,name='about'),
  path('add_stock/<user_name>',views.add_stock,name='add_stock'),
  path('delete/<stock_id>/<user_name>/',views.delete,name='delete'),
  path('get_stocks/<user_name>',views.getstocks,name='get_stock'),
  path('autocomplete',views.autocomplete,name='autocomplete'),
  path('fullStockDetail/<ticker>',views.fullStockDetail,name='fullStockDetail')
]
