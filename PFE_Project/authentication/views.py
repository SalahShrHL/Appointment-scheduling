from django.shortcuts import render, redirect
from .forms import *
from Patient.models import *
from django.contrib.auth import authenticate,get_user_model,login,logout
# from django.contrib.auth.models import User
from django.contrib import messages

def Login(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        if user.is_patient :
            return redirect('H_patient')
        if user.is_doctor :
            return redirect('H_doctor')
        if user.is_admin :
            messages.warning(request, 'invalid user or password')
            return render(request, "authentication/login.html")
    if form.errors :
        context = {
        'form': form,
        }
        messages.warning(request, 'invalid user or password')
        return render(request, "authentication/login.html", context)
    context = {
    'form': form,
    }
    return render(request, "authentication/login.html", context)

def Login_admin(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        if user.is_admin : 
            return redirect('H_admin')
        else:
            messages.warning(request, 'invalid user or password')
            return render(request, "authentication/adminLogin.html", context)
    if form.errors :
        context = {
        'form': form,
        }
        messages.warning(request, 'invalid user or password')
        return render(request, "authentication/adminLogin.html", context)
    context = {
    'form': form,
    }
    return render(request, "authentication/adminLogin.html", context)

def initiateP_Profil(email):
    w = wilaya.objects.get(wilaya="Adrar")
    Patient(img_patient="anonymous_user.jpg", nomPatient=" ", prenomPatient=" ",
    date_naiss="1960-1-1", blood="A+", genre="male", emailPatient=email, telephone=0, 
    Address=" ", wilaya=w).save()

def RegisterP(request):
    User=get_user_model()
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        #user register------------------------
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.email, password=password)
        #user login---------------------------
        login(request, new_user)
        #transform the account to patient account------------
        email = form.cleaned_data.get('email')
        u = User.objects.get(email = email)
        u.is_patient = True
        u.save()
        #create an empty profil for the new patient---------------
        initiateP_Profil(email)
        Notification(user = User.objects.get(is_admin = True), Date=datetime.datetime.now(), content="Un nouveau patient sest inscrit", sender=request.user).save()
        return redirect('profil_patient')
    if form.errors :
        context = {
        'form': form,
        }
        messages.warning(request, 'user already exists')
        return render(request, "authentication/register.html", context)
    context = {
        'form': form,
    }
    return render(request, "authentication/register.html", context)

def initiateD_Profil(email,nom,prenom,tel,nom_cabinet):
    w = wilaya.objects.get(wilaya="Adrar")
    cabinet = Medecin(img_medecin = "anonymous_user.jpg", email=email, nom_medecin =nom , 
    prenom_medecin = prenom, telephone = tel, genre ="male", date_naiss = "1960-1-1", 
    NomCabinet = nom_cabinet, addresse = " ", wilaya = w)
    cabinet.save()

def RegisterD(request):
    User=get_user_model()
    form = UserRegisterForm(request.POST or None) 
    print("---------------i m here-----------------")
    print(form)

    if form.is_valid():
        #user register------------------------
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.email, password=password)
        #user login---------------------------
        login(request, new_user)
        #transform the account to doctor account------------
        email = form.cleaned_data.get('email')
        u = User.objects.get(email = email)
        u.is_doctor = True
        u.save()
        #initiate a new profil for the new doctor---------------
        initiateD_Profil(email,form.cleaned_data.get('last_name'),form.cleaned_data.get('first_name'),form.cleaned_data.get('num_tel'),form.cleaned_data.get('nom_cabinet'))
        Notification(user = User.objects.get(is_admin = True), Date=datetime.datetime.now(), content="Un nouveau médecin s'est inscrit", sender=request.user).save()
        return redirect('profile_doctor')
    if form.errors :
        print("-------i m here ------------")
        print(form.errors)
        context = {
        'form': form,
        }
        messages.warning(request, 'utilisateur existe déja!')
        return render(request, "authentication/registerD.html", context)
    context = {
        'form': form,
    }
    return render(request, "authentication/registerD.html", context)

def Logout(request):
    logout(request)
    return redirect('home')