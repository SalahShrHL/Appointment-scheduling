from django.urls import URLPattern, path
from . import views
from .models import *

urlpatterns=[
    #---------------------------------------------------Générale------------------------------------------------------
    path('', views.index, name='home'),
    path('getUser/<str:email>', views.getUser, name="GetUser"),
    path('delImg/<int:id>', views.deleteImg, name="DelImg"),

    #---------------------------------------------------Patient------------------------------------------------------
    path('chercheCabinet/', views.search, name="cherCabinet"),
    path('Acceuil/', views.indexP, name="H_patient"),
    path('P_profil/', views.getP_Profil, name="profil_patient"),
    path('updateP_Profil/', views.updateP_Profil, name="update_profil_patient"),
    path('GetRV/<int:id>', views.getRV, name="GetListRV"),
    path('prendreRV/', views.prendRV, name="PrendRV"),
    path('ProfilD/<int:id>', views.ProfilD, name="ProfilD"),
    path('deleteRV/', views.deleteRV, name="DeleteRV"),
    path('Bookmark/<int:id>', views.bookmark, name="Bookmark"),
    path('writeComment/<int:id>', views.writeComment, name="Comment"),
    path('FavoriteDoc/', views.GetListFav, name="FavDoc"),
    path('FilterSearch/', views.SFilter, name="FilterSearch"),

    #---------------------------------------------------Doctor------------------------------------------------------
    path('AcceuilD/', views.indexD, name="H_doctor"),
    path('D_profil/', views.getD_Profil, name="profile_doctor"),
    path('updateD_Profil/', views.updateD_Profil, name="update_profil_doctor"),
    path('getTimingSchedual/', views.get_TimingSchedule, name="GetTimingSchedual"),
    path('addTimingSchedual/', views.add_TimingSchedule, name="AddTimingSchedual"),
    path('DelTimingSchedual/<int:id>', views.del_TimingSchedule, name="DelTimingSchedual"),
    path('DelTimingSchedual/', views.upd_TimingSchedule, name="UpdTimingSchedual"),
    path('GetPaitentList/', views.get_patient_list, name="GetPatientList"),
    path('GetRVList/', views.getListRV, name="GetListRV"),
    path('GetD_RVList/', views.getD_RD, name="D_RV_LIST"),
    path('annulerRV/', views.annulerRV, name="AnnulerRDV"),
    path('Dashboard/', views.getDashboard, name="Dashboard"),
    path('LibererJournee/', views.Liberer, name="LibererJournee"),
    path('GetAvis/', views.GetAvis, name="GetAvis"),

    #---------------------------------------------------Admin------------------------------------------------------
    path('A_panel/', views.index_admin, name="H_admin"),
    path('A_patients/', views.getPatientsA, name="PatientsAdmin"),
    path('A_doctors/', views.getDoctorsA, name="DoctorsAdmin"),
    path('A_specialites/', views.getspecialitesA, name="specialitesAdmin"),
    path('Add_specialites/', views.addSpecialite, name="AddSpecialite"),
    path('edit_specialites/', views.editSpecialite, name="EditSpecialite"),
    path('del_specialites/', views.delSpecialite, name="DeltSpecialite"),
    path('ClearRDV/', views.Clear, name="ClearRDV")
]