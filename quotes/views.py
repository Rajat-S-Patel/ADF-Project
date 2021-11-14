from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from quotes.models import Stock
from django.contrib.auth import  login
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.detail import DetailView
from Auth.models import CustomUser
from .utils import *


from .form import StockForm
from Auth.forms import PersonalInfoUpdateForm
import csv
from django.contrib.auth.decorators import login_required

# Create your views here.
API_CACHE={}
CURR_API='pk_fac4ed3466ac44c994f3d8ee26bf41a2'


stock_list=[]
    
def main(request):
    return redirect('signin')


def autocomplete(request):
    
    global stock_list
    if(stock_list==[]):
        with open('quotes/assets/stocks.csv','r') as f:
            reader = csv.reader(f)
            for i in reader:
                stock_list.append(i[1])
    return JsonResponse(stock_list,safe=False)
    # return redirect('home')

def home(request,ticker=None):
    # = 
    import requests
    import json
    global stock_list,API_CACHE
    if(stock_list==[]):
        with open('quotes/assets/stocks.csv','r') as f:
           
            reader = csv.reader(f)
            for i in reader:
                stock_list.append(i[1])

    if(ticker!=None):
        if(ticker not in API_CACHE.keys()):
            api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/batch?types=quote&range=1m&last=100&token="+CURR_API)
            API_CACHE[ticker]=api_request
        else:api_request=API_CACHE[ticker]

        try:
            api=json.loads(api_request.content)
            payload=onload(ticker)
            response={"api":api['quote'],"ticker":ticker,"nav":"home","news":None}
            response['chart']=payload['chart']
            response['forecast']=payload['forecast']
            return render(request,'../templates/home.html',response)

            
        except Exception as e:
            api="Error..."
            ticker="Error..."
            news="Error..."
            return render(request,'../templates/home.html')


    if(request.method=='POST'):
        ticker=request.POST['ticker']
       
        try:
            ticker=ticker[ticker.index("(")+1:len(ticker)-1]

        except ValueError:
            return render(request,'../templates/home.html')

      
        #api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_fac4ed3466ac44c994f3d8ee26bf41a2")
        if(ticker not in API_CACHE.keys()):
            api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/batch?types=quote&range=1m&last=100&token="+CURR_API)
            API_CACHE[ticker]=api_request

        else:api_request=API_CACHE[ticker]
        try:
            api=json.loads(api_request.content)
            payload=onload(ticker)
            response={"api":api['quote'],"ticker":ticker,"nav":"home","news":None}
            response['chart']=payload['chart']
            response['forecast']=payload['forecast']
   
            return render(request,'../templates/home.html',response)

            
        except Exception as e:
            print(e)
            api="Error..."
            ticker="Error..."
            news="Error..."
            return render(request,'../templates/home.html')

        
    else:
       
        ticker="ndaq"
        
        if(ticker not in API_CACHE.keys()):
            api_request=requests.get("https://cloud.iexapis.com/stable/stock/ndaq/batch?types=quote&range=1m&last=100&token="+CURR_API)
            API_CACHE[ticker]=api_request
        else:
            api_request=API_CACHE[ticker]
        try:
            api=json.loads(api_request.content)
            print(api)
            payload=onload(ticker)
            response={"api":api['quote'],"ticker":ticker,"nav":"home","news":None}
            response['chart']=payload['chart']
            response['forecast']=payload['forecast']
           
        
            
        except Exception as e:
            print(e)
            api="Error..."
        
        return render(request,'../templates/home.html',response)

def stockChartApi(request,ticker):
    ticker= ticker if ticker is  None else 'ndaq'
    payload=onload(ticker)
    return JsonResponse(payload)
 
def about(request):
    return render(request,'about.html',{"nav":'about'})

@login_required(login_url='signin')
def getstocks(request):
    import requests
    import json
    
    if request.user == None:
        return messages.error(request,'Please login to view this page')
    ticker=Stock.objects.all().filter(user=request.user.id)
    output=[]
    for ticker_item in  ticker:
        api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token="+CURR_API)
        temp=json.loads(api_request.content)
        output.append((temp,ticker_item))
    return render(request,'add_stock.html',{"output":output,"nav":"add_stock"})

@login_required(login_url='signin')
def add_stock(request):   
    import requests
    import json

    if(request.method=='POST'):
        ticker=None
        try:
            ticker=request.POST['ticker']
            ticker=ticker[ticker.index("(")+1:len(ticker)-1]

        except ValueError:
            pass
        if(ticker is None):
            messages.error(request,"Invalid Ticker")
        stock=None
        try:
            stock=Stock.objects.get(ticker=ticker)
        except Stock.DoesNotExist:
            stock=Stock(ticker=ticker)
            stock.save()
            
        
        stock.user.add(request.user)
        return redirect('get-stock')

def fullStockDetail(request,ticker):
    import requests
    import json
    
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker) + "/quote?token=pk_c36651668be94b01a673aaf2684bdbe3")

    try:
        api = json.loads(api_request.content)
        
    except Exception as e:
        api = "Error.."
    return render(request, 'fullStockDetail.html', {'api': api,'ticker':ticker})

@login_required(login_url='signin')
def delete(request,stock_id):
    item=Stock.objects.get(pk=stock_id)
    item.user.remove(request.user)
    messages.success(request,("Stock has been deleted"))
    return redirect('get-stock')

def register(request):
    if request.method == "GET":
        return render(
            request, "register.html",
            
        )
    elif request.method == "POST":
        form = PersonalInfoUpdateForm(request.POST)
    
        if form.is_valid():
            user = form.save()
            login(request, user)
       
            return redirect('home')


class ProfileView(LoginRequiredMixin,DetailView):
    model=CustomUser
    template_name='profile.html'
    context_object_name='user'
    login_url='signin'

    def get(self,request):
        print('inside request')
        return render(request,self.template_name,{'user':request.user})