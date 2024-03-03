
from django.urls import path
from  simples_pages.views import get_list, details_song, search_song

urlpatterns = [
    path('index/', get_list, name="get_list"),
    path('details/<str:title>/', details_song, name="details_song"),
    path('search/', search_song, name="search_song"),
]




