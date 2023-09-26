from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from mydjproject import models as mydjproject_models
from . import models

#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/' :
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware


def adminhome(request):
    #print(request.session["sunm"])
    return render(request,"adminhome.html",{"sunm":request.session["sunm"]})

def manageusers(request):
    uDetails=mydjproject_models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"uDetails":uDetails,"sunm":request.session["sunm"]})

def manageuserstatus(request):
    regid=int(request.GET.get("regid"))
    #print(request.regid)
    s=request.GET.get("s")
    if s=="verify":
        mydjproject_models.Register.objects.filter(regid=regid).update(status=1)
    elif s=="block":
        mydjproject_models.Register.objects.filter(regid=regid).update(status=0)
    else:
        mydjproject_models.Register.objects.filter(regid=regid).delete()
    
    return redirect("/myadmin/manageusers/")

def addcategory(request):
    if request.method=="GET":
        return render(request,"addcategory.html",{"output":"","sunm":request.session["sunm"]})
    else:
        catname=request.POST.get("catname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.Category(catname=catname,caticonname=filename)
        p.save()
        return render(request,"addcategory.html",{"output":"Category Add Successfully","sunm":request.session["sunm"]})
    
def addsubcategory(request):
    clist=models.Category.objects.all()
    if request.method=="GET": 
        return render(request,"addsubcategory.html",{"output":"","clist":clist,"sunm":request.session["sunm"]})
    else:
        catname=request.POST.get("catname")
        subcatname=request.POST.get("subcatname")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.SubCategory(catname=catname,subcatname=subcatname,subcaticonname=filename)
        p.save()
        return render(request,"addsubcategory.html",{"output":"Sub Category Add Successfully","clist":clist,"sunm":request.session["sunm"]})
    