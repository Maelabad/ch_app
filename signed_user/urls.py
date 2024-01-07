from django.urls import path
from  signed_user.views import sget_list, sdetails_song, ssearch_song

urlpatterns = [
    path('', sget_list, name="sget_list"),
    path('details/<str:title>/', sdetails_song, name="details_song"),
    path('search/', ssearch_song, name="search_song"),
    #Ce serait bien d'avoir le str rechercher
]
