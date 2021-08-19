from django.db.models import fields
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from quotes.models import Stock
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .form import StockForm,CustomUserCreationForm
import pandas as pd
# Create your views here.

CURR_API='pk_fac4ed3466ac44c994f3d8ee26bf41a2'

# def login(request):
#     return render(request,'registration/login.html')

stock_list=[]
    
def main(request):
    return render(request,'main.html')

def autocomplete(request):
    
    # if('term' in request.GET):
        # print('sds')
    global stock_list
    if(stock_list==[]):
        stock_list=list(pd.read_csv('quotes/assets/stocks.csv').values[:,1])
    return JsonResponse(stock_list,safe=False)
    # return redirect('home')

def home(request,ticker=None):
    # = 
    import requests
    import json
    global stock_list
    if(stock_list==[]):
        stock_list=list(pd.read_csv('quotes/assets/stocks.csv').values[:,1])

    if(ticker!=None):
        api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/batch?types=quote,news&range=1m&last=100&token="+CURR_API)
        try:
            api=json.loads(api_request.content)
            return render(request,'../templates/home.html',{"api":api['quote'],"ticker":ticker,"nav":"home","news":api['news']})

            
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

        api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/batch?types=quote,news&range=1m&last=100&token="+CURR_API)
        try:
            api=json.loads(api_request.content)
            return render(request,'../templates/home.html',{"api":api['quote'],"ticker":ticker,"nav":"home","news":api['news']})

            
        except Exception as e:
            api="Error..."
            ticker="Error..."
            news="Error..."
            return render(request,'../templates/home.html')

        
    else:
       
        #api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_fac4ed3466ac44c994f3d8ee26bf41a2")
        ticker="ndaq"



        api_request=requests.get("https://cloud.iexapis.com/stable/stock/ndaq/batch?types=quote,news&range=1m&last=100&token="+CURR_API)
        try:
            api=json.loads(api_request.content)
        
            
        except Exception as e:
            print(e)
            api="Error..."
        
        return render(request,'../templates/home.html',{"api":api['quote'],"ticker":ticker,"nav":"home","news":api['news']})

    
    
def about(request):
    return render(request,'about.html',{"nav":'about'})


def getstocks(request,user_name):
    import requests
    import json

    ticker=Stock.objects.all().filter(user=user_name)
    output=[]
    for ticker_item in  ticker:
        api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token="+CURR_API)
        temp=json.loads(api_request.content)
        output.append((temp,ticker_item))
    return render(request,'add_stock.html',{"output":output,"nav":"add_stock"})

def add_stock(request,user_name):   
    import requests
    import json

    if(request.method=='POST'):
        dic={'ticker':request.POST['ticker'],'user':request.POST['user']}
        try:
            ticker=request.POST['ticker']
            ticker=ticker[ticker.index("(")+1:len(ticker)-1]
            dic['ticker']=ticker
        except ValueError:
            pass

        form=StockForm(dic or None)
        
        if(form.is_valid()):
            form.save()
            messages.success(request,("Stock has been added Succesfully!"))
            return redirect('get_stock',user_name=user_name)

    # else:
    #     ticker=Stock.objects.all()
    #     output=[]
    #     for ticker_item in  ticker:
    #         api_request=requests.get("https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_fac4ed3466ac44c994f3d8ee26bf41a2")
    #         temp=json.loads(api_request.content)
    #         output.append((temp,ticker_item))
    #     return render(request,'add_stock.html',{"output":output})

def fullStockDetail(request,ticker):
    import requests
    import json
    
    api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker) + "/quote?token=pk_c36651668be94b01a673aaf2684bdbe3")

    try:
        api = json.loads(api_request.content)
        
    except Exception as e:
        api = "Error.."
    return render(request, 'fullStockDetail.html', {'api': api,'ticker':ticker})



def delete(request,stock_id,user_name):
    item=Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,("Stock has been deleted"))
    return redirect('get_stock',user_name=user_name)

def register(request):
    if request.method == "GET":
        return render(
            request, "register.html",
            
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
    
        if form.is_valid():
            user = form.save()
            login(request, user)
       
            return redirect('home')


        

        

