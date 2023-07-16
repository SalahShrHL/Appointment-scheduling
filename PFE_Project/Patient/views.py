from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
from datetime import *
import datetime
from .forms import *
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Max, Min, Avg, F, Q
import math 
# General -----------------------------------------------------------------------------------------
def index(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
            return redirect('H_patient')
        else:
            return redirect('H_doctor')
    w = wilaya.objects.all()
    s = specialite.objects.all()
    context = {'w':w, 's':s}
    return render(request, 'index.html',context)

# Patient -----------------------------------------------------------------------------------------
def indexP(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
            w = wilaya.objects.all()
            s = specialite.objects.all()
            i = Patient.objects.get(emailPatient = request.user)
            n = Notification.objects.filter(user = request.user).order_by('-Date')
            notif = serializers.serialize("json", n)
            if n.exists():
                empty = 'false'
            else: 
                empty = 'true'
            for notification in n:
                if notification.new == True :
                    notification.new = False
                    notification.save()
                    
            n = i.nomPatient
            p = i.prenomPatient
            i = i.img_patient.url  
            context = {'w':w, 's':s, 'i':i, 'p':p, 'n':n, 'notif': notif, 'empty': empty}
            return render(request, 'index_patient.html', context)
    return render(request, 'authentication/login.html')

def search(request):
    cabinets = Medecin.objects.all()
    w = request.GET['wilaya']
    s = request.GET['specialite']
    search_name = request.GET['nomCabinet']
    context = {'wilaya': w, 'specialite': s, 'search_name': search_name}
    if w != 'Wilaya':
        W = wilaya.objects.get(wilaya = w)
        cabinets = cabinets.filter(wilaya = W)
        if s != 'Spécialité':
            S = specialite.objects.get(specialite = s)
            cabinets = cabinets.filter(specialite = S)
            # context = {'s':S}
        if search_name != '':
            cabinets = cabinets.filter(NomCabinet__contains = search_name)
        nbr = cabinets.count
        if request.user.is_authenticated : 
            i = Patient.objects.get(emailPatient = request.user)
            n = Notification.objects.filter(user = request.user).order_by('-Date')
            notif = serializers.serialize("json", n)
            if n.exists():
                empty = 'false'
            else: 
                empty = 'true'
            for notification in n:
                if notification.new == True :
                    notification.new = False
                    notification.save()
            n = i.nomPatient
            p = i.prenomPatient
            i = i.img_patient.url 
            context.update({'c':cabinets, 'i':i, 'p':p, 'n':n,'nbr':nbr,'w':W, 'empty': empty, 'notif': notif})
        else :
             context.update({'c':cabinets,'nbr':nbr,'w':W})
        return render(request,'search.html', context)
    else:
        return redirect('home')

def SFilter(request):
    cabinets = Medecin.objects.all()
    w = request.GET['wilaya']
    s = request.GET['specialite']
    search_name = request.GET['nomCabinet']
    context = {'wilaya': w, 'specialite': s, 'search_name': search_name}
    #filter wilaya--------------
    W = wilaya.objects.get(wilaya = w)
    cabinets = cabinets.filter(wilaya = W)
    #filter specialite--------------
    if s != 'Spécialité':
        S = specialite.objects.get(specialite = s)
        cabinets = cabinets.filter(specialite = S)
        # context = {'s':S}
    #filter nom cabinet--------------
    if search_name != '':
        cabinets = cabinets.filter(NomCabinet__contains = search_name)
    #filter genre--------------
    if not (request.GET.get('male', 'off') == 'on' and request.GET.get('female', 'off') == 'on'):
        if request.GET.get('male', 'off') == 'on':
            cabinets = cabinets.filter(genre='male')
        if request.GET.get('female', 'off') == 'on':
            cabinets = cabinets.filter(genre='female')

    nbr = cabinets.count

    if request.user.is_authenticated : 
        i = Patient.objects.get(emailPatient = request.user)
        n = Notification.objects.filter(user = request.user).order_by('-Date')
        notif = serializers.serialize("json", n)
        if n.exists():
            empty = 'false'
        else: 
            empty = 'true'
        for notification in n:
            if notification.new == True :
                notification.new = False
                notification.save()
        n = i.nomPatient
        p = i.prenomPatient
        i = i.img_patient.url 
        context.update({'c':cabinets, 'i':i, 'p':p, 'n':n,'nbr':nbr,'w':W, 'empty': empty, 'notif': notif})
    else :
        context.update({'c':cabinets,'nbr':nbr,'w':W})
        
    return render(request, 'search.html', context)

def getP_Profil(request):
    u = Patient.objects.get(emailPatient = request.user)
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    w = wilaya.objects.all()
    c = serializers.serialize("json", commune.objects.all())
    u_json = serializers.serialize("json", Patient.objects.filter(emailPatient = request.user))
    age = 0
    age = date.today().year - u.date_naiss.year
    context = {'u':u, 'age':age, 'w':w, 'c':c, 'u_json': u_json, 'empty': empty, 'notif': notif}
    return render(request, 'profile_setings.html', context)

def updateP_Profil(request):
    if request.method == "POST": 
        user_old = Patient.objects.get(emailPatient = request.user)
        form = profil_P_form(request.POST, request.FILES, instance= user_old)
        if form.is_valid():
            form.save()
            # messages.success(request, "changes were succesfully saved")
    return redirect('H_patient')

def getRV(request, id):
    if request.user.is_authenticated:
        if request.user.is_patient:
            U = Patient.objects.get(emailPatient = request.user)
            M = Medecin.objects.get(id = id)
            avi = Avi.objects.filter(cabinet = M).count()
            n = Notification.objects.filter(user = request.user).order_by('-Date')
            notif = serializers.serialize("json", n)
            if n.exists():
                empty = 'false'
            else: 
                empty = 'true'
            for notification in n:
                if notification.new == True :
                    notification.new = False
                    notification.save()
                    
            motif = Motif.objects.all()
            type = type_consultation.objects.filter(medecin = M)
            type = serializers.serialize("json", type)
            medecin = Medecin.objects.get(id = id)
            rv = RV.objects.filter(medecin = medecin).order_by('Date','heure') 
            #spliting according to days of the week
            dimenche = rv.filter(Date__week_day = 1)
            lundi = rv.filter(Date__week_day = 2)
            mardi = rv.filter(Date__week_day = 3)
            mercredi = rv.filter(Date__week_day = 4)
            jeudi = rv.filter(Date__week_day = 5)
            vendredi = rv.filter(Date__week_day = 6)
            samedi = rv.filter(Date__week_day =7)
            #serializing
            Dimenche = serializers.serialize("json", dimenche)
            Lundi = serializers.serialize("json", lundi)
            Mardi = serializers.serialize("json", mardi)
            Mercredi = serializers.serialize("json", mercredi)
            Jeudi = serializers.serialize("json", jeudi)
            Vendredi = serializers.serialize("json", vendredi)
            Samedi = serializers.serialize("json", samedi)
            context = {
                'u': U,
                'm': M,
                'avi': avi,
                'notif': notif,
                'empty': empty,
                'motif' : motif,
                'type' : type,
                'Dimenche': Dimenche,
                'Lundi': Lundi,
                'Mardi': Mardi,
                'Mercredi': Mercredi,
                'Jeudi': Jeudi,
                'Vendredi': Vendredi,
                'Samedi': Samedi
            }
            return render(request, 'booking.html', context)
    return redirect('Login')

def prendRV(request):
    U = Patient.objects.get(emailPatient = request.user)
    rv = RV.objects.get(id = request.POST.get('id_RV'))
    if(request.POST.get('Aprenom') == ''):
        rv_valide = RV_valide(patient=U, medecin=rv.medecin,
        dateRV=rv.Date, heure=rv.heure, type_consultation=rv.type, 
        status="confirmé", nom_payer=request.POST.get('nom'), 
        prenom_payer=request.POST.get('prenom'), 
        num_carte=request.POST.get('num_carte'))
    else:
        try:
            user = Anonymous.objects.get(nom=request.POST.get('Anom'), prenom = request.POST.get('Aprenom'))
        except:
            user = Anonymous()
            user.nom = request.POST.get('Anom')
            user.prenom = request.POST.get('Aprenom')
            date = datetime.datetime.strptime(request.POST.get('ADate_naiss'), "%d/%m/%Y")
            user.date_naiss = date
            user.save()
            user = Anonymous.objects.get(nom=request.POST.get('Anom'), prenom=request.POST.get('Aprenom'))
        
        rv_valide = RV_valide(patient=U, medecin=rv.medecin,
        dateRV=rv.Date, heure=rv.heure, type_consultation=rv.type, 
        status="confirmé", nom_payer=request.POST.get('nom'), 
        prenom_payer=request.POST.get('prenom'), 
        num_carte=request.POST.get('num_carte'),
        pour_anonymous = True,
        anonymous_patient = user)

    rv_valide.save()
    Notification(user = rv.medecin.email, Date=datetime.datetime.now(), content="<strong>"+U.nomPatient+" "+U.prenomPatient+"</strong>"+" "+ "a pris un RDV", sender=U.emailPatient).save()
    rv.delete()
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    context = {
        'u': U,
        'RV': rv_valide,
        'notif': notif,
        'empty': empty
    }
    return render(request, 'booking_Success.html', context)

def getListRV(request):
    U = Patient.objects.get(emailPatient = request.user)
    list = RV_valide.objects.filter(patient__emailPatient = request.user)
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    context = {'u': U, 'list': list, 'notif': notif, 'empty': empty}
    return render(request, 'listRDV.html', context)

def deleteRV(request):
    id_RDV = request.POST.get('ID_RDV')
    U = Patient.objects.get(emailPatient = request.user)
    RDV = RV_valide.objects.get(id = id_RDV)
    Notification(user = RDV.medecin.email, Date=datetime.datetime.now(), content="<strong>"+U.nomPatient+" "+U.prenomPatient+"</strong>"+" "+ "a annulé un RDV", sender = U.emailPatient).save()
    RV(
        Date = RDV.dateRV,
        type = RDV.type_consultation,
        heure = RDV.heure,
        duree = RDV.type_consultation.duree,
        medecin = RDV.medecin
    ).save()
    RDV.status = "annulé"
    RDV.save()
    messages.success(request, "le rendez_vous a été annulé avec successé")
    return redirect('GetListRV')

def getUser(request, email):
    User = get_user_model()
    u = User.objects.get(email = email)
    if u.is_doctor:
        d = Medecin.objects.filter(email = email)
    else:
        d = Patient.objects.filter(emailPatient = email)
    d = serializers.serialize("xml", d)
    return HttpResponse(d)  

def ProfilD(request, id):
    M = Medecin.objects.get(id = id)
    #business hours---------------------
    slots = type_consultation.objects.filter(medecin__id = id)
    #dimenche
    try :
        min = slots.filter(j = "Dimenche").aggregate(Min('start')).get('start__min')
        max = slots.filter(j = "Dimenche").aggregate(Max('end')).get('end__max')
        Dimenche = min.strftime("%H:%M:%S")+" - "+max.strftime("%H:%M:%S")
    except:
        Dimenche = "closed"
    #lundi
    try :
        min = slots.filter(j = "Lundi").aggregate(Min('start')).get('start__min')
        max = slots.filter(j = "Lundi").aggregate(Max('end')).get('end__max')
        Lundi = min.strftime("%H:%M:%S")+" - "+max.strftime("%H:%M:%S")
    except:
        Lundi = "closed"
    #mardi
    try :
        min = slots.filter(j = "Mardi").aggregate(Min('start')).get('start__min')
        max = slots.filter(j = "Mardi").aggregate(Max('end')).get('end__max')
        Mardi = min.strftime("%H:%M:%S")+" - "+max.strftime("%H:%M:%S")
    except:
        Mardi = "closed"
    #mercredi
    try :
        min = slots.filter(j = "Mercredi").aggregate(Min('start')).get('start__min')
        max = slots.filter(j = "Mercredi").aggregate(Max('end')).get('end__max')
        Mercredi = min.strftime("%H:%M:%S")+" - "+max.strftime("%H:%M:%S")
    except:
        Mercredi = "closed"
    #jeudi
    try :
        min = slots.filter(j = "Jeudi").aggregate(Min('start')).get('start__min')
        max = slots.filter(j = "Jeudi").aggregate(Max('end')).get('end__max')
        Jeudi = min.strftime("%H:%M:%S")+" - "+max.strftime("%H:%M:%S")
    except:
        Jeudi = "closed"
    #vendredi
    try :
        min = slots.filter(j = "Vendredi").aggregate(Min('start')).get('start__min')
        max = slots.filter(j = "Vendredi").aggregate(Max('end')).get('end__max')
        Vendredi = min.strftime("%H:%M:%S")+" - "+max.strftime("%H:%M:%S")
    except:
        Vendredi = "closed"
    #samedi
    try :
        min = slots.filter(j = "Samedi").aggregate(Min('start')).get('start__min')
        max = slots.filter(j = "Samedi").aggregate(Max('end')).get('end__max')
        Samedi = min.strftime("%H:%M:%S")+" - "+max.strftime("%H:%M:%S")
    except:
        Samedi = "closed"

    #reviews-----------------------------------
    medecin = Medecin.objects.get(id = id)
    A = Avi.objects.filter(cabinet = medecin)

    context = { 'm': M, 
                'a': A,
                'Dimenche': Dimenche,
                'Lundi': Lundi,
                'Mardi': Mardi,
                'Mercredi': Mercredi,
                'Jeudi': Jeudi,
                'Vendredi': Vendredi,
                'Samedi': Samedi
                }

    if request.user.is_authenticated and request.user.is_patient:
        U = Patient.objects.get(emailPatient = request.user)
        #notifications
        n = Notification.objects.filter(user = request.user).order_by('-Date')
        notif = serializers.serialize("json", n)
        if n.exists():
            empty = 'false'
        else: 
            empty = 'true'
        for notification in n:
            if notification.new == True :
                notification.new = False
                notification.save()
        #favoré ou non ----------------------------
        try:
            MedecinFavori.objects.get(patient__emailPatient = request.user, medecin__id= id) 
            fav = True
        except:
            fav = False
        context.update({'empty': empty, 'notif':notif, 'fav': fav, 'u':U})

        return render(request, 'AuthDoctor_profil.html', context)
    return render(request, 'doctor_profil.html', context)   

def bookmark(request, id):
    try:
        b = MedecinFavori.objects.get(medecin__id = id, patient__emailPatient = request.user)
        b.delete()
    except:
        MedecinFavori(patient = Patient.objects.get(emailPatient = request.user), medecin= Medecin.objects.get(id = id)).save()
        
    return HttpResponse()

def writeComment(request, id):
    rates = {'star-1':1, 'star-2':2, 'star-3':3, 'star-4':4, 'star-5':5}
    M = Medecin.objects.get(id = id)
    avis = Avi.objects.filter(cabinet__id = id)
    try:
        A = Avi.objects.get(cabinet = Medecin.objects.get(id = id), patient = Patient.objects.get(emailPatient = request.user))
        A.delete()
        if avis.count == 0:
            M.rating = 0
        M.save()
    except:
        pass
    finally:
        Avi(cabinet = Medecin.objects.get(id = id),
        patient = Patient.objects.get(emailPatient = request.user),
        content = request.POST.get('comment-content'),
        rating = rates.get(request.POST.get('rating')),
        date = datetime.datetime.now().date()
        ).save()
        if M.rating == 0:
            M.rating = rates.get(request.POST.get('rating'))
        else:
            temp = avis.aggregate(Avg('rating')).get('rating__avg')
            M.rating = math.floor(temp)
        M.save()
    return redirect('ProfilD',id)

def GetListFav(request):
    U = Patient.objects.get(emailPatient = request.user)
    #notifications------------
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    #cabinet favoreé--------------
    c = MedecinFavori.objects.filter(patient__emailPatient = request.user)
    
    context = {
        'u': U,
        'empty': empty,
        'notif': notif,
        'c': c
    }
    return render(request, 'listDocFav.html', context)

# Doctor -----------------------------------------------------------------------------------------
def indexD(request): 
    if request.user.is_authenticated:
        if request.user.is_doctor:
            u = Medecin.objects.get(email = request.user)

            #notifications--------
            n = Notification.objects.filter(user = request.user).order_by('-Date')
            notif = serializers.serialize("json", n)

            if n.exists():
                empty = 'false'
            else:
                empty = 'true'

            for notification in n:
                if notification.new == True :
                    notification.new = False
                    notification.save()
            #/notifications--------

            #events -------
            objs = RV_valide.objects.filter(medecin__email = request.user).filter(Q(status='confirmé') | Q(status='annulé', dateRV=datetime.datetime.now().date()))
            list = []
            classNames = {'annulé':'bg-danger','confirmé':'bg-primary'}
            for obj in objs:
                start = datetime.datetime.combine(obj.dateRV, obj.heure)
                end = start + timedelta(minutes=obj.type_consultation.duree)
                list.append({'title':'RDV', 'start':str(start), 'end':str(end), 'className':classNames[obj.status]})
            #/events -------

            context = {'u':u, 'notif': notif, 'empty': empty, 'list': list}
            return render(request, 'doctor/index_doctor.html',context)
    return render(request, 'authentication/login.html')

def getD_Profil(request):
    u = Medecin.objects.get(email = request.user)
    w = wilaya.objects.all()
    c = commune.objects.all()
    c = serializers.serialize("json", commune.objects.all())
    #in order to avoid parsing problem in js (because of googlemaps_iframe)
    temp = Medecin.objects.filter(email = request.user)
    for t in temp:
        t.googlemaps_iframe = ""
    u_json = serializers.serialize("json", temp)
    s = specialite.objects.all()
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)

    if n.exists():
        empty = 'false'
    else:
        empty = 'true'

    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()

    context = {'u':u, 's':s, 'w':w, 'c':c, 'u_json':u_json, 'notif':notif, 'empty':empty}
    return render(request, 'doctor/profile_setings.html',context)

def updateD_Profil(request):
    if request.method == "POST": 
        user_old = Medecin.objects.get(email = request.user)
        form = profil_D_form(request.POST, request.FILES, instance= user_old)
        if form.is_valid():
            form.save()
        else:
            messages.warning(request, form.errors.as_text())
            return redirect('profile_doctor')
    return redirect('H_doctor')

def deleteImg(request, id):
    temp = Medecin.objects.get(email = request.user)
    if id == 1:
        temp.img1 = "cabinet/anonymous_clinic_Y8q2eiZ.png"
    elif id == 2:
        temp.img2 = "cabinet/anonymous_clinic_Y8q2eiZ.png"
    else:
        temp.img3 = "cabinet/anonymous_clinic_Y8q2eiZ.png"
    temp.save()
    return redirect('profile_doctor')

def get_TimingSchedule(request):
    #data-------------------------------
    dimenche = "Dimenche"
    lundi = "Lundi"
    mardi = "Mardi"
    mercredi = "Mercredi"
    jeudi = "Jeudi"
    vendredi = "Vendredi"
    samedi = "Samedi"

    cabinet = Medecin.objects.get(email = request.user)

    DimencheTiming = type_consultation.objects.filter(medecin = cabinet, j = dimenche)
    LundiTiming = type_consultation.objects.filter(medecin = cabinet, j = lundi)
    MardiTiming = type_consultation.objects.filter(medecin = cabinet, j = mardi)
    MercrediTiming = type_consultation.objects.filter(medecin = cabinet, j = mercredi)
    JeudiTiming = type_consultation.objects.filter(medecin = cabinet, j = jeudi)
    VendrediTiming = type_consultation.objects.filter(medecin = cabinet, j = vendredi)
    SamediTiming = type_consultation.objects.filter(medecin = cabinet, j = samedi)

    list_motif = Motif.objects.all()
    liste_motif_json = serializers.serialize("json", list_motif)
    data = serializers.serialize("json", type_consultation.objects.all())

    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()

    context = {
        'D' : DimencheTiming,
        'L' : LundiTiming,
        'Ma' : MardiTiming,
        'Me' : MercrediTiming,
        'J' : JeudiTiming,
        'V' : VendrediTiming,
        'S' : SamediTiming,
        'u' : cabinet,
        'data': data,
        'motifs' : list_motif,
        'motifs_js' : liste_motif_json,
        'notif': notif,
        'empty': empty
    }
    return render(request, 'doctor/schedual_timing.html', context)

def createRV(motif):
    date = (datetime.datetime.today()+timedelta(days=1)).date()
    date_end = date + timedelta(days=30)
    while(date<date_end):
        if(date.weekday() == motif.getDay()):
            if(str(type(motif.start))=="<class 'datetime.time'>"):
                start = datetime.datetime.strptime(str(motif.start), "%H:%M:%S").time()
                end = datetime.datetime.strptime(str(motif.end), "%H:%M:%S").time()
            else:
                start = datetime.datetime.strptime(motif.start, "%H:%M").time()
                end = datetime.datetime.strptime(motif.end, "%H:%M").time()
            while(start<=end):
                RV(Date=date, type=motif, heure=start, duree=motif.duree, medecin=motif.medecin).save()
                minutes = int(motif.duree)
                # here i stat var became of type datetime (it was datetime.time) 
                # in order to add it to timedelta than convert it to datetime.time again
                start = (datetime.datetime.combine(datetime.datetime(1,1,1), start) + timedelta(minutes=minutes)).time()
        date = date + timedelta(days=1)
    return 0

def updateRV(id):
    deleteSlot(id)
    motif = type_consultation.objects.get(id = id)
    createRV(motif = motif)
    return 0

def deleteSlot(id):
    motif = type_consultation.objects.get(id = id)
    RV.objects.filter(type = motif).delete()
    return 0

def add_TimingSchedule(request):
    form = Motif_form(request.POST)
    if form.is_valid:
        M = request.POST.get('motif')
        M = Motif.objects.get(id = M)
        D = request.POST.get('duree')
        P = request.POST.get('prix')
        email = request.user
        C = Medecin.objects.get(email = email)
        S = request.POST.get('start')
        E = request.POST.get('end')
        jour = request.POST.get('jour')
        motif = type_consultation(motif = M, duree = D, prix = P, medecin = C, start = S, end = E, j = jour)
        motif.save()
        messages.success(request, 'slot added seccessfuly')
        createRV(motif = motif)
    else: 
        messages.warning(request, 'one or many invalid informations!')  
    return redirect('GetTimingSchedual')

def del_TimingSchedule(request, id):
    deleteSlot(id)
    M = type_consultation.objects.get(id = id).delete()
    messages.success(request, 'slot was deleted successfuly')
    return redirect('GetTimingSchedual')

def upd_TimingSchedule(request):
    old_motif = type_consultation.objects.get(id = request.POST.get('id'))
    cabinet = Medecin.objects.get(id = old_motif.medecin.id)
    motif = Motif.objects.get(nomMotif = request.POST.get('motif'))
    new_data = {
        'motif': motif,
        'duree': request.POST.get('duree'),
        'prix': request.POST.get('prix'),
        'j': old_motif.j,
        'medecin': cabinet,
        'start': request.POST.get('start'),
        'end': request.POST.get('end')
    }
    form = Motif_form(new_data, instance = old_motif)
    if form.is_valid():
        messages.success(request, "the slot was updated successfuly")
        form.save()
        updateRV(request.POST.get('id'))
    return redirect('GetTimingSchedual')

def get_patient_list(request):
    u = Medecin.objects.get(email = request.user)
    rendez_vous = RV_valide.objects.filter(medecin = u).values_list('patient', flat=True).distinct()
    list = []
    for id in rendez_vous:
        list.append(id)

    patient_list = Patient.objects.filter(id__in = list)
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    context = {
        'u' : u,
        'P' : patient_list,
        'notif': notif,
        'empty': empty
    }
    return render(request, 'doctor/liste_patients.html', context)

def getD_RD(request):
    u = Medecin.objects.get(email = request.user)
    #notifications-------------
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    #list RDVs----------------------
    list = RV_valide.objects.filter(medecin__email = request.user, dateRV__gte = datetime.datetime.now().date()).exclude(Q(status="completé") & Q(status="annulé"))
    today = datetime.datetime.now().date()
    context = {'u':u, 'notif':notif, 'empty':empty, 'list':list, 'today':today}
    return render(request, 'doctor/listRDV.html', context)

def annulerRV(request):
    U = Medecin.objects.get(email = request.user)
    RDV = RV_valide.objects.get(id = request.POST.get('ID_RDV'))
    RDV.status = "annulé"
    RDV.save()
    RV(Date=RDV.dateRV, type=RDV.type_consultation, heure=RDV.heure, duree=RDV.type_consultation.duree, medecin=RDV.medecin).save()
    Notification(user = RDV.patient.emailPatient, Date=datetime.datetime.now(), content="<strong>"+U.NomCabinet+"</strong>"+" "+ "a annulé un RDV,veuillez choisir un autre RDV (gratuitement), pour plus dinformations veuillez contacter le médecin", sender = U.email).save()
    messages.success(request, "le rendez_vous a été annulé avec successé, et une notification a été envoyé au patient")
    # send_mail(
    # 'Rendez_vous annulé',
    # 'votre rendez_vous a été annulé a cause dune urgence, veuillez choisir un autre rendez_vous (gratuitment), pour plus dinformation veuillez contacter la cabinet',
    # 'zking1094@gmail.com',
    # ['zizo.fillali@gmail.com'],
    # fail_silently=False,
    # )
    return redirect('D_RV_LIST')

def getDashboard(request):
    u = Medecin.objects.get(email = request.user)
    #notifications-------------
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    #statistics----------------
    total_patient = RV_valide.objects.filter(status ="completé", medecin__email=request.user).values_list('patient', flat=True).distinct().count()
    total_RDV = RV_valide.objects.filter(status = "completé", medecin__email=request.user).count()
    today_date = datetime.datetime.now().date()
    today_patient = RV_valide.objects.filter(status = "confirmé", dateRV=today_date, medecin__email=request.user).values_list('patient', flat=True).distinct().count()
    #patient per year-----------
    Plist = []
    year = RV_valide.objects.filter(medecin__email=request.user).aggregate(Min('dateRV')).get('dateRV__min').year

    while year <= datetime.datetime.now().year:
        a = RV_valide.objects.filter(status ="completé", dateRV__year = year, medecin__email=request.user).values_list('patient', flat=True).distinct().count()
        obj = {'year': year, 'patients': a}
        Plist.append(obj)
        year = year +1

    #patients's gender ---------------
    Glist = []
    year = RV_valide.objects.filter(medecin__email=request.user).aggregate(Min('dateRV')).get('dateRV__min').year

    while year <= datetime.datetime.now().year:
        a = RV_valide.objects.filter(status ="completé", dateRV__year = year, patient__genre = "male", medecin__email=request.user).values_list('patient', flat=True).distinct().count()
        b = RV_valide.objects.filter(status ="completé", dateRV__year = year, patient__genre = "female", medecin__email=request.user).values_list('patient', flat=True).distinct().count()
        obj = {'year': year, 'males': a, 'females':b}
        Glist.append(obj)
        year = year +1

    #patient's motif----------------------
    Mlist = []
    temp = []
    motifs = RV_valide.objects.filter(medecin__email=request.user).annotate(motif=F('type_consultation__motif__nomMotif')).values('motif')
    for motif in motifs :
        temp.append(motif.get('motif'))
    temp = list(dict.fromkeys(temp))
    
    for name in temp:
        a = RV_valide.objects.filter(medecin__email=request.user, type_consultation__motif__nomMotif = name).count()
        obj = {'label':name, 'value':a}
        Mlist.append(obj)
    
    #appointments list-------------------
    list_RDV = RV_valide.objects.filter(medecin__email = request.user)

    context = {'u':u,
            'empty':empty,
            'notif':notif, 
            'total_patient':total_patient, 
            'today_patient':today_patient,
            'today_date': today_date,
            'total_RDV':total_RDV,
            'Plist': Plist,
            'Glist': Glist,
            'Mlist': Mlist, 
            'list': list_RDV
            }
    return render(request, 'doctor/Dashboard.html', context)

def Liberer(request):
    if request.method == 'POST':
        date = datetime.datetime.strptime(request.POST.get('date_journée'), "%d/%m/%Y")
        heureD = request.POST.get('heure_debut')
        heureF = request.POST.get('heure_debut')
        RDVs = RV.objects.filter(medecin__email = request.user, Date= date)
        if heureD != '':
            RDVs = RDVs.filter(Q(heure__gte = heureD) & Q(heure__lte = heureF))
        RDVs.delete()
        messages.success(request,'opération a été réalisé avec successé')
        return redirect('GetTimingSchedual')
    messages.warning(request, 'quelque chose sest mal passé')
    return redirect('GetTimingSchedual')

def GetAvis(request):
    u = Medecin.objects.get(email = request.user)
    #notifications-------------
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    
    #avis----------------------
    avis = Avi.objects.filter(cabinet__email = request.user)
    context = {
        'u': u,
        'empty': empty,
        'notif': notif,
        'avis': avis
    }
    return render(request, 'doctor/reviews.html', context)

#Admin ------------------------------------------------------------------------------------------------

def index_admin(request):
    if request.user.is_authenticated and request.user.is_admin:
        #notifications ------
        n = Notification.objects.filter(user = request.user).order_by('-Date')
        notif = serializers.serialize("json", n)
        if n.exists():
            empty = 'false'
        else: 
            empty = 'true'
        for notification in n:
            if notification.new == True :
                notification.new = False
                notification.save()
        p = Patient.objects.all().count()
        d = Medecin.objects.all().count()
        r = RV_valide.objects.filter(status = "completé").count()

    #statistics--------------------------

    #patient per year-----------
        Plist = []
        year = Patient.objects.all().aggregate(Min('Date_signIn')).get('Date_signIn__min').year

        while year <= datetime.datetime.now().year:
            a = a = Patient.objects.filter(Date_signIn__year = year).count()
            obj = {'year': year, 'patients': a}
            Plist.append(obj)
            year = year +1

    #doctor per year-----------
        Dlist = []
        year = Medecin.objects.all().aggregate(Min('Date_signIn')).get('Date_signIn__min').year

        while year <= datetime.datetime.now().year:
            a = Medecin.objects.filter(Date_signIn__year = year).count()
            obj = {'year': year, 'medecins': a}
            Dlist.append(obj)
            year = year +1

    #rating--------------------
    #chaque année on veut savoir la cabinet qui avait le meilleure rating
    
        context = {
            'patient_total':p,
            'medecin_total':d,
            'RDV_total':r,
            'Plist': Plist,
            'Dlist': Dlist,
            'empty':empty,
            'notif': notif
        }
        return render(request, 'A/index_admin.html', context)
    else:
        return redirect('Login_admin')

def getPatientsA(request):
    patients = Patient.objects.all()
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    
    context = {
        'notif': notif,
        'empty': empty,
        'patients': patients
    }
    return render(request, 'A/Patients.html', context)

def getDoctorsA(request):
    doctors = Medecin.objects.all()
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()
    context = {
        'notif': notif,
        'empty': empty,
        'doctors': doctors
    }
    return render(request, 'A/Doctors.html', context)

def getspecialitesA(request):
    specialites = specialite.objects.all()
    n = Notification.objects.filter(user = request.user).order_by('-Date')
    notif = serializers.serialize("json", n)
    if n.exists():
        empty = 'false'
    else: 
        empty = 'true'
    for notification in n:
        if notification.new == True :
            notification.new = False
            notification.save()

    context = {'specialites': specialites, 'notif': notif, 'empty': empty}
    return render(request, 'A/specialites.html', context)

def addSpecialite(request):
    if request.method == "POST":
        form = specialiteForm(request.POST)
        if form.is_valid:
            form.save()
    return redirect('specialitesAdmin')

def editSpecialite(request):
    if request.method == "POST":
        s = specialite.objects.get(id = request.POST.get('id'))
        form = specialiteForm(request.POST, instance=s)
        if form.is_valid:
            form.save()
    return redirect('specialitesAdmin')

def delSpecialite(request):
    id = request.POST.get('id')
    obj = specialite.objects.get(id = id).delete()
    return redirect('specialitesAdmin')

def Clear(request):
    #part 1 ------------
    today = datetime.datetime.now().date()
    RDV = RV_valide.objects.filter(dateRV__lt = today, status = "confirmé", heure__lt = datetime.datetime.now().time())
    for R in RDV :
        R.status = "completé"
        R.save()
        
    #part 2 ------------
    RV.objects.filter(Date__lte = today , heure__lt = datetime.datetime.now().time()).delete()
    #part 3 ------------
    yesterday = today - timedelta(days=1)
    date = yesterday + timedelta(days=30)
    days_of_week = ["Dimenche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
    jour = days_of_week[date.weekday()]
    types = type_consultation.objects.filter(j = jour)

    for type in types:
        start = type.start
        end = type.end
        while(start<=end):
            RV(Date=date, type=type, heure=start, duree=type.duree, medecin=type.medecin).save()
            minutes = type.duree
            # start = start + timedelta(minutes=minutes)
            start = (datetime.datetime.combine(datetime.datetime(1,1,1), start) + timedelta(minutes=minutes)).time()
    messages.success(request, 'opération est terminé avec successé')
    return redirect('H_admin')