from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from django.conf import settings

from . import models
import time
from mydjproject import models as mydjproject_models
from myadmin import models as myadmin_models

media_url=settings.MEDIA_URL

#middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=='/user/viewtenders/' or request.path=='/user/viewsubcat/':
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware


def userhome(request):
    return render(request,"userhome.html",{"sunm":request.session["sunm"]})

def viewtenders(request):
    clist=myadmin_models.Category.objects.all()
    return render(request,"viewtenders.html",{"clist":clist,"media_url":media_url,"sunm":request.session["sunm"]})

def viewsubcat(request):
    catname=request.GET.get("catname")
    clist=myadmin_models.Category.objects.all()
    sclist=myadmin_models.SubCategory.objects.filter(catname=catname)
    return render(request,"viewsubcat.html",{"catname":catname,"sclist":sclist,"media_url":media_url,"clist":clist,"sunm":request.session["sunm"]})

def funds(request):
    paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID="sb-d0fan22346738@business.example.com"
    #sb-hwkj123537359@personal.example.com
    amt=100
    return render(request,"funds.html",{"sunm":request.session["sunm"],"paypalURL":paypalURL,"paypalID":paypalID,"amt":amt})

def payment(request):
    uid=request.GET.get("uid")
    amt=request.GET.get("amt")
    
    p=models.Payment(uid=uid,amt=amt,info=time.asctime())
    p.save()
    return redirect("/user/success/")


def success(request):
    return render(request,"success.html",{"sunm":request.session["sunm"]})

def cancel(request):
    return render(request,"cancel.html",{"sunm":request.session["sunm"]})

def viewfunds(request):
    fDetails=models.Payment.objects.all()
    return render(request,"viewfunds.html",{"sunm":request.session["sunm"],"fDetails":fDetails})

def cpuser(request):
    if request.method=="GET":
        return render(request,"cpuser.html",{"sunm":request.session["sunm"]})
    else:
        sunm=request.session["sunm"]
        opass=request.POST.get("opass")
        npass=request.POST.get("npass")
        cnpass=request.POST.get("cnpass")
        
        userDetails=mydjproject_models.Register.objects.filter(email=sunm,password=opass)
        if len(userDetails)>0:
            if npass==cnpass:
                mydjproject_models.Register.objects.filter(email=sunm).update(password=cnpass)
                return render(request,"cpuser.html",{"sunm":sunm,"output":"Password changed successfully...."})
            else:
                return render(request,"cpuser.html",{"sunm":sunm,"output":"New & confirm password mismatch"})
        else:
            return render(request,"cpuser.html",{"sunm":sunm,"output":"Invalid Old Password"})
            

            
     