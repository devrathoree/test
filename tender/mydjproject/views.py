from django.shortcuts import render , redirect

from . import models
import time

from . import emailAPI

from . import resetemailAPI

#middleware to check session for user routes
def sessioncheckmydjproject_middleware(get_response):
	def middleware(request):
		if request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
			request.session['sunm']=None
			request.session['srole']=None
			response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

def home(request):
    return render(request,"home.html")


def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def service(request):
    return render(request,"service.html")

def register(request):
    if request.method=="GET":
        return render(request,"register.html",{"output":""})
    else:
        #to receive post data
        name=request.POST.get("name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        mobile=request.POST.get("mobile")
        address=request.POST.get("address")
        city=request.POST.get("city")
        gender=request.POST.get("gender")
        
        
        p=models.Register(name=name,email=email,password=password,mobile=mobile,
            address=address,city=city,gender=gender,status=0,role="user",info=time.asctime())
        
        p.save()
        
        emailAPI.sendMail(email,password)
        
        return render(request,"register.html",{"output":"user regitered successfully"})
        
def login(request):
    if request.method=="GET":
        return render(request,"login.html",{"output":""})
    else:
        #to receive post data
        email=request.POST.get("email")
        password=request.POST.get("password")
             
        userDetails=models.Register.objects.filter(email=email,password=password,status=1)

        if len(userDetails)>0:
            
            # to store user details in session
            request.session["sunm"]=userDetails[0].email            
            request.session["srole"]=userDetails[0].role
            
            if userDetails[0].role=="admin":
                return redirect("/myadmin/")
            else:
                return redirect("/user/")
        else:
            return render(request,"login.html",{"output":"invalid user or not verified"})

def verify(request):
    vemail=request.GET.get("vemail")
    models.Register.objects.filter(email=vemail).update(status=1)
    return redirect("/login/")

def reset(request):
    if request.method=="GET":
        return render(request,"reset.html",{"output":""})
    else:
        email=request.POST.get("email")
        if models.Register.objects.filter(email=email):
            resetemailAPI.sendMail(email)
            return render(request,"reset.html",{"output":"Please check your mail"})
        else:
            return render(request,"reset.html",{"output":"Invalid mail id"})
    
def resetpass(request):
    if request.method=="GET":
        vemail=request.GET.get("vemail")
        return render(request,"resetpass.html",{"output":"","vemail":vemail})
    else:
        npass=request.POST.get("npass")
        cnpass=request.POST.get("cnpass")
        vemail=request.POST.get("vemail")
       
        if npass==cnpass:
            models.Register.objects.filter(email=vemail).update(password=cnpass)
            return render(request,"login.html",{"output":"Password changed successfully...."})
        else:
            return render(request,"resetpass.html",{"output":"New & confirm password mismatch"})
