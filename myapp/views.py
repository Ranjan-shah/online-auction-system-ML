from django.contrib.messages.api import success
from django import views
from django.db.models.fields import DateField
from django.http import HttpResponse
from django.core.checks import messages
from django.shortcuts import redirect,render
from django.views import View
from .models import product,Buyer,bidding
from django.contrib.auth.models import User
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import pytz
from django.utils import timezone
from itertools import chain
from django.conf import settings
from django.core.mail import send_mail

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np

import pandas as pd
import pickle
with open('model_pickle', 'rb') as f:
    reloadmodel = pickle.load(f)

with open('model_pickleb', 'rb') as f:
    reloadmodel = pickle.load(f)


def send_email(name,email):
    subject='Bid Submission'
    message=f'Hello {name},Your bid has been submitted successfully'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)
# Create your views here.
utc=pytz.UTC
class product_View(View):
    def get(self,request):
        vehicle=product.objects.filter(category='vehicle',status='onAuction',verified=True)
        realstate=product.objects.filter(category='real state',status='onAuction',verified=True)
        electronics=product.objects.filter(category='electronics',status='onAuction',verified=True)
        sports=product.objects.filter(category='sports',status='onAuction',verified=True)
        jewelry=product.objects.filter(category='jewelry',status='onAuction',verified=True)
        return render(request,'index.html',{'vehicle':vehicle,'realstate':realstate,'electronics':electronics,'sports':sports,'jewelry':jewelry})
        

class mybiddingView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            myuser = User.objects.get(id=request.user.id)
            newuser=myuser
            myproduct=product.objects.get(pk=pk)
            myprice=myproduct.base_price
            price=myprice+myprice/10
            myobj=bidding.objects.create(current_price=myprice,updated_price=price)
            myobj.save()
            myobj.username.add(myuser)
            myobj.product.add(myproduct)
            myproduct.base_price=price
            myproduct.save()
            myproduct.bids=myproduct.bids+1
            myproduct.save()
            send_email(newuser.first_name,newuser.email)
            return redirect('/')
        else:
            return redirect('login')

class myprofile(View):
    def get(self,request):
        print(request.user.id)
        profile=Buyer.objects.get(pk=request.user.id)
        return render(request,'profile.html',{'profile':profile})


def get_updated(request):
    if request.method=="POST":
        myfile=request.FILES['mydoc']
        profile=Buyer.objects.get(user=request.user)
        profile.profile_img=myfile
        profile.save()
        return redirect('profile')
        
    else:    
        return render(request,'form.html')

class get_details(View):
    def get(self,request):
        myuser=request.user.id
        obj1=bidding.objects.filter(username__id=myuser)
        mypk=[]
        for x in obj1:
            mypk.append(x.pk)
        myobj=bidding.objects.filter(pk__in=mypk)
        myproducts=product.objects.filter(bidding__pk__in=mypk)
        return render(request,'bid-details.html',{'detail':myobj,'result':myproducts})

class listing_page(View):
    def get(self,request):
        query = request.GET.get("query", None)
        products=product.objects.filter(status='onAuction',verified=True)
        if query is not None:
            products = products.filter(title__icontains=query)
        return render(request,'listing.html',{'products':products, 'query':query})

# class electronics_page(View):
def electronics(request):
    electronics=product.objects.filter(category='electronics',status='onAuction',verified=True)
    return render(request,'electronics.html',{'electronics':electronics})

def vehicle(request):
    vehicle=product.objects.filter(category='vehicle',status='onAuction',verified=True)
    return render(request,'vehicle.html',{'vehicle':vehicle})    

def realstate(request):
    realstate=product.objects.filter(category='real state',status='onAuction',verified=True)
    return render(request,'realstate.html',{'realstate':realstate})  

def sports(request):
    sports=product.objects.filter(category='sports',status='onAuction',verified=True)
    return render(request,'sports.html',{'sports':sports})  

def jewelry(request):
    jewelry=product.objects.filter(category='jewelry',status='onAuction',verified=True)
    return render(request,'jewelry.html',{'jewelry':jewelry})  

      

class contact_page(View):
    def get(self,request):
        query = request.GET.get("query", None)
        return render(request,'contact.html',{ 'query':query})

def carpredict(request):
    return render(request,'carpredict.html')

def carpredicts(request):
    if request.method == 'POST':
        temp = {}
        temp['carmodel'] = request.POST.get('carmodel')
        temp['caryear'] = request.POST.get('caryear')
        temp['cartransmission'] = request.POST.get('cartransmission')
        temp['carkilometer'] = request.POST.get('carkilometer')
        temp['carfueltype'] = request.POST.get('carfueltype')
        temp['cartax'] = request.POST.get('cartax')
        temp['carmpg'] = request.POST.get('carmpg')
        temp['carengine'] = request.POST.get('carengine')
        
    testData = pd.DataFrame({'x':temp}).transpose()
    prctval = reloadmodel.predict(testData)[0]

    targetval = temp
    
    mol_f = {"0":"Audi", "1":"Datsun", "2":"Ford", "3":"Honda", "4":"Hyundai", "5":"MarutiSuzuki", "6":"Suzuki", "7":"Jeep", "8":"Kia", "9":"Mahindra", "10":"Nissan",
     "11":"Toyota", "12":"Tata", "13":"Renault", "14":"BMW", "15":"MercedesBenz", "16":"Mitsubishi", "17":"Fiat", "18":"Mini", "19":"Cheverolet",
      "20":"RollsRoyce", "21":"Mazda", "22":"Ambassador", "23":"Lexus", "24": "Jaguar", "25":"Volkswagon"}
    trans_f = {"0":"Manual", "1":"Automatic", "2":"Semi-Auto"}
    fuel_f = {"0":"Diesel", "1":"Petrol", "2":"Hybrid"}
    
    if temp['carmodel']:
        targetval['carmodel'] = mol_f[temp['carmodel']]
    if temp['cartransmission']:
        targetval['cartransmission'] = trans_f[temp['cartransmission']]
    if temp['carfueltype']:
        targetval['carfueltype'] = fuel_f[temp['carfueltype']]
    
    targetval['target'] = prctval

    return render(request, 'carpredict.html', targetval)       



def housepredict_page(request):
    return render(request, "housepredict.html")

def resultp(request):
    data = pd.read_csv("D:\\auction\\myapp\\Nepal_Housing.csv")
    data = data.drop(['Address'], axis=1)
    X = data.drop('Price', axis=1)
    Y = data['Price']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.30)   
    model = LinearRegression()
    model.fit(X_train, Y_train)

    var1 = float(request.GET['n1'])
    var2 = float(request.GET['n2'])
    var3 = float(request.GET['n3'])
    var4 = float(request.GET['n4'])
    var5 = float(request.GET['n5'])

    pred = model.predict(np.array([var1, var2, var3, var4, var5]).reshape(1,-1))
    pred = round(pred[0])

    price = "The Predicted Price is RS "+str(pred)


    return render (request, "housepredict.html", {"result2":price})    



   

def bikepredict(request):
    return render(request,'bikepredict.html')

def bikepredicts(request):
    if request.method == 'POST':
        temp = {}
        temp['bikemodel'] = request.POST.get('bikemodel')
        temp['bikeyear'] = request.POST.get('bikeyear')
        temp['biketransmission'] = request.POST.get('biketransmission')
        temp['bikekilometer'] = request.POST.get('bikekilometer')
        temp['bikefueltype'] = request.POST.get('bikefueltype')
        temp['biketax'] = request.POST.get('biketax')
        temp['bikempg'] = request.POST.get('bikempg')
        temp['bikeengine'] = request.POST.get('bikeengine')
        
    testData = pd.DataFrame({'x':temp}).transpose()
    prctval = reloadmodel.predict(testData)[0]

    targetval = temp
    
    mol_f = {"0":"Hero", "1":"Honda", "2":"TVS", "3":"Yamaha", "4":"Bajaj", "5":"Suzuki", "6":"RoyalEnfield", "7":"Jawa", "8":"KTM", "9":"Mahindra", "10":"Kawasaki", "11":"Beneli", "12":"Italijet", "13":"Ducati", "14":"BMW", "15":"HarleyDavidson",
     "16":"Aprilia", "17":"Triumph", "18":"CFMoto", "19":"Husqverna", "20":"SYM", "21":"LML", "22":"BSA", "23":"Vespa", "24": "Zontes", "25":"HeroHonda"}
    trans_f = {"0":"Manual", "1":"Automatic"}
    fuel_f = { "0":"Petrol"}
    
    if temp['bikemodel']:
        targetval['bikemodel'] = mol_f[temp['bikemodel']]
    if temp['biketransmission']:
        targetval['biketransmission'] = trans_f[temp['biketransmission']]
    if temp['bikefueltype']:
        targetval['bikefueltype'] = fuel_f[temp['bikefueltype']]
    
    targetval['target'] = prctval

    return render(request, 'bikepredict.html', targetval)








	