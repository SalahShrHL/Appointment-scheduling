from django.db import models
import datetime

class specialite(models.Model):
   specialite = models.CharField(max_length=400)
   def __str__(self):
        return self.specialite

class wilaya(models.Model):
    wilaya = models.CharField(max_length=20)
    def __str__(self):
        return self.wilaya

class commune(models.Model):
    commune = models.CharField(max_length=20)
    wilaya = models.ForeignKey(wilaya, on_delete=models.CASCADE)
    def __str__(self):
        return self.commune

blood_type = (("A+","A+"),("A-","A-"),("B+","B+"),("B-","B-"),("AB+","AB+"),("AB-","AB-"),("O+","O+"),("O-","O-"))
genre = (("female","female"),("male","male"))
class Medecin(models.Model):
    img_medecin = models.ImageField(null=True, upload_to='medecin', blank=True)
    nom_medecin = models.CharField(null=True, blank=True, max_length=20)
    prenom_medecin = models.CharField(null=True, blank=True, max_length=20)
    genre = models.CharField(max_length=10, choices=genre, null=True, blank=True)
    date_naiss = models.DateField(null=True, blank=True)
    biographie = models.TextField(null=True, blank=True)
    # rempalçant = models.BooleanField(default=False)
    googlemaps_iframe = models.CharField(max_length=1000, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    NomCabinet = models.CharField(max_length=60, unique=True, blank=True, null=True)
    telephone = models.PositiveBigIntegerField(blank=True, null=True)
    addresse = models.CharField(max_length=60, null=True, blank=True)
    specialite = models.ForeignKey(specialite, on_delete=models.CASCADE, null=True, blank=True)
    img1 = models.ImageField(null=True, upload_to='cabinet', blank=True, default="anonymous_clinic.jpg")
    img2 = models.ImageField(null=True, upload_to='cabinet', blank=True, default="anonymous_clinic.jpg")
    img3 = models.ImageField(null=True, upload_to='cabinet', blank=True, default="anonymous_clinic.jpg")
    wilaya = models.ForeignKey(wilaya, on_delete=models.CASCADE, null=True, blank=True)
    commune = models.ForeignKey(commune, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(default=0.0, null=True, blank=True)
    Date_signIn = models.DateField(null=True, blank=True, default=datetime.datetime.now().date())
    def __str__(self):
       return self.email
    def changeFormat(self):
        return self.date_naiss.strftime("%m-%d-%Y") 

class Patient(models.Model):
    img_patient =  models.ImageField(null=True, upload_to='patient', blank=True)
    nomPatient = models.CharField(max_length=20, null=True, blank=True)
    prenomPatient = models.CharField(max_length=20, null=True, blank=True)
    date_naiss = models.DateField(null=True, blank=True)
    blood = models.CharField(null=True, blank=True, choices=blood_type, max_length=4)
    genre = models.CharField(max_length=10, choices=genre, null=True, blank=True)
    emailPatient = models.EmailField(unique=True)
    telephone = models.PositiveBigIntegerField(blank=True, null=True)
    Address = models.CharField(max_length=60, blank=True, null=True)
    commune = models.ForeignKey(commune, null=True, blank=True, on_delete=models.CASCADE)
    wilaya = models.ForeignKey(wilaya, null=True, blank=True, on_delete=models.CASCADE)
    Date_signIn = models.DateField(null=True, blank=True, default=datetime.datetime.now().date())
    def __str__(self):
        return self.emailPatient
    def changeFormat(self):
        return self.date_naiss.strftime("%m-%d-%Y")
    def age(self):
        current_year = datetime.datetime.now().year
        return current_year-self.date_naiss.year

class Anonymous(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    date_naiss = models.DateField(null=True, blank=True)

class Motif(models.Model):
    nomMotif = models.CharField(max_length=60, null=True, blank=True)
    def __str__(self):
        return self.nomMotif

duree = ((15,15),(30,30),(45,45),(60,60),(90,90))
jours = (("Dimenche","Dimenche"),("Lundi","Lundi"),
("Mardi","Mardi"),("Mercredi","Mercredi"),
("Jeudi","Jeudi"),("Vendredi","Vendredi"),
("Samedi","Samedi"))
class type_consultation(models.Model):
    motif = models.ForeignKey(Motif, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    duree = models.IntegerField(choices=duree)
    prix = models.PositiveIntegerField()
    j = models.CharField(max_length=10, choices=jours, null=True, blank=True)
    start = models.TimeField(default="0:0")
    end = models.TimeField(default="0:0")
    def __str__(self):
        return self.j+' '+self.motif.nomMotif
    def getDay(self):
        days = {
            "Lundi" : 0,
            "Mardi" : 1,
            "Mercredi" : 2,
            "Jeudi" : 3,
            "Vendredi" : 4,
            "Samedi" : 5,
            "Dimenche" : 6
        }
        return days.get(self.j)

class RV(models.Model):
    Date = models.DateField(null=True, blank=True)
    type = models.ForeignKey(type_consultation, on_delete=models.CASCADE, null=True, blank=True)
    heure = models.TimeField(default="0:0")
    duree = models.PositiveIntegerField(null=True, blank=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, null=True, blank=True)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    def french_Date(self):
        year = self.Date.year
        month = self.Date.month
        day = self.Date.day
        return str(day)+"-"+str(month)+"-"+str(year)
    def french_time(self):
        return self.heure.strftime("%H:%M:%S")

status = (("completé","completé"),("annulé","annulé"),("confirmé","confirmé"))
class RV_valide(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    dateRV = models.DateField()
    heure = models.TimeField(default="0:0")
    type_consultation = models.ForeignKey(type_consultation, on_delete=models.CASCADE)
    nom_payer = models.CharField(max_length=20, null=True, blank=True)
    prenom_payer = models.CharField(max_length=20, null=True, blank=True)
    num_carte = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=15, choices=status)
    pour_anonymous = models.BooleanField(default=False)
    anonymous_patient = models.ForeignKey(Anonymous, on_delete=models.CASCADE, null=True, blank=True)
    def french_Date(self):
        year = self.dateRV.year
        month = self.dateRV.month
        months = ["Jan", "Fév", "Mars", "Avr", "Mai", "Juin", "Jui", "Aôut", "Sep","Oct", "Nov", "Dec"]
        day = self.dateRV.day
        return str(day)+" "+str(months[month-1])+" "+str(year)
    def french_time(self):
        return self.heure.strftime("%H:%M:%S")
    
    def day_name(self):
        days = ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"]
        return str(days[self.dateRV.weekday()])
        
class Avi(models.Model):
    cabinet = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Commentaire '+self.cabinet.NomCabinet+'--'+self.patient.nomPatient

    def french_Date(self):
        year = self.date.year
        month = self.date.month
        months = ["Jan", "Fév", "Mars", "Avr", "Mai", "Juin", "Jui", "Aôut", "Sep","Oct", "Nov", "Dec"]
        day = self.date.day
        return str(day)+" "+str(months[month-1])+" "+str(year)

class Notification(models.Model):
    user = models.EmailField(null=True, blank=True)
    Date = models.DateTimeField(null=True, blank=True)
    content = models.CharField(max_length=200, null=True, blank=True)
    sender = models.EmailField(null=True, blank=True)
    new = models.BooleanField(default=True)
    def french_Date(self):
        year = self.Date.year
        month = self.Date.month
        day = self.Date.day
        return str(day)+"-"+str(month)+"-"+str(year)
    def __str__(self):
        return self.user

class MedecinFavori(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, null=True, blank=True)
    