from django import contrib
from django.urls import path,include
from . import views
urlpatterns = [
  path('',views.main,name='main'),
  path('accounts/',include('django.contrib.auth.urls')),
  path('home/',views.home,name='home'),
   path('home/<ticker>',views.home,name='home_ticker'),
  path('about',views.about,name='about'),
  path('add-stock/',views.add_stock,name='add-stock'),
  path('delete/<stock_id>',views.delete,name='delete'),
  path('get-stocks/',views.getstocks,name='get-stock'),
  path('profile/', views.ProfileView.as_view(),name='profile'),
  path('autocomplete',views.autocomplete,name='autocomplete'),
  path('fullStockDetail/<ticker>',views.fullStockDetail,name='fullStockDetail'),
  path('getStockChart/<ticker>',views.stockChartApi,name="stocksChart"),
]
