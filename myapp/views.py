from django.shortcuts import render,redirect
from .forms import *
from django.core.mail import send_mail
import random
import requests
from FinalProject import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    user=request.session.get('user')
    return render(request,'index.html',{'user':user})

@login_required(login_url='/login')
def notes(request):
    msg=""
    user=request.session.get('user')
    if request.method=='POST':
        newnotes=notesForm(request.POST,request.FILES)
        if newnotes.is_valid():
            newnotes.save()
            print("Your notes has been submitted!")
            msg="Your notes has been submitted!"
        else:
            print(newnotes.errors)
            msg="Error!Something went wrong...Try again"
    return render(request,'notes.html',{'user':user,'msg':msg})

def profile(request):
    msg=""
    user=request.session.get('user')
    userid=request.session.get('userid')
    cid=usersignup.objects.get(id=userid)
    if request.method=='POST':
        updateData=updateForm(request.POST)
        if updateData.is_valid():
            updateData=updateForm(request.POST,instance=cid)
            updateData.save()
            print("Your Profile has been updated!")
            msg="Your Profile has been updated!"
            return redirect('/')
        else:
            msg="Error!Profile updation faild...Try again!"
            print(updateData.errors)
    return render(request,'profile.html',{'user':user,'msg':msg,'cid':cid})

def about(request):
    user=request.session.get('user')
    return render(request,'about.html',{'user':user})

def contact(request):
    user=request.session.get('user')
    if request.method=='POST':
        newcontact=contactForm(request.POST)
        if newcontact.is_valid():
            newcontact.save()
            print("Your feed has been submitted!")
        else:
            print(newcontact.errors)
    return render(request,'contact.html',{'user':user})

def login(request):
    msg=""
    if request.method=='POST':
        unm=request.POST['username']
        pas=request.POST['password']

        user=usersignup.objects.filter(username=unm,password=pas)
        userid=usersignup.objects.get(username=unm)
        print("Userid:",userid.id)
        if user:
            print("Login Successfull!")
            msg="Login Successfull!"
            request.session['user']=unm
            request.session['userid']=userid.id
            return redirect('/')
        else:
            print("Error!Login faild...Try again")
            msg="Error!Login faild...Try again"
    return render(request,'login.html',{'msg':msg})

def otpverify(request):
    msg=""
    global otp
    print("Your OTP:",otp)
    if request.method=='POST':
        if request.POST['otp']==str(otp):
            print("Verification Successfull!")
            msg="Verification Successfull!"
            return redirect('login')
        else:
            msg="Verification Faild...Please try again!"
    return render(request,'otpverify.html',{'msg':msg})

def signup(request):
    msg=""
    if request.method=='POST':
        newuser=signupForm(request.POST)
        username=""
        if newuser.is_valid():
            username=newuser.cleaned_data.get('username')
            try:
                usersignup.objects.get(username=username)
                print("Username is already exists!")
                msg="Username is already exists!"
            except usersignup.DoesNotExist:
                    newuser.save()
                    print("Signup Successfully!")
                    msg="Signup Successfully!"

                    #Send Email
                    global otp
                    otp=random.randint(11111,99999)
                    sub="Your One Time Password!"
                    msg=f"Dear User\n\nThank you for using our services, Your account has been created with us!\n\nFor Verification purpose, Your One time password is\n{otp}.\n\nThanks & Regrads\nTOPS Technologies - Rajkot\n+91 9724799469 | sanket.tops@gmail.com"
                    from_ID=settings.EMAIL_HOST_USER
                    to_ID=[request.POST['username']]
                    send_mail(subject=sub,message=msg,from_email=from_ID,recipient_list=to_ID)

                    #Send SMS

                    """url = "https://www.fast2sms.com/dev/bulkV2"
                    querystring = {"authorization":"KEodGeCxJPkWAFHQUYtS86Rbmrv1MyuViag4hs7N2DujvzKSw5MN9mRryb3LC4DsIHiWph78","variables_values":f"{otp}","route":"otp","numbers":"7623904602,9313623232,9313819231"}
                    headers = {
                        'cache-control': "no-cache"
                    }
                    response = requests.request("GET", url, headers=headers, params=querystring)
                    print(response.text)"""

                    return redirect('otpverify')
        else:
            print(newuser.errors)
    return render(request,'signup.html',{'msg':msg})

def userlogout(request):
    logout(request)
    return redirect('/login')