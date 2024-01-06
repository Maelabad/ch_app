from django.urls import path
from  signed_user.views import sget_list, details_song, search_song

urlpatterns = [
    path('', sget_list, name="sget_list"),
    path('details/<str:title>/', details_song, name="details_song"),
    path('search/', search_song, name="search_song"),
    #Ce serait bien d'avoir le str rechercher
]
