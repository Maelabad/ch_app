from django.urls import path
from  signed_user.views import sget_list, sdetails_song, ssearch_song, sadd_song, smodify_song, authentication

urlpatterns = [
    path('index/', sget_list, name="sget_list"),
    path('authentication/', authentication, name="authentication"),
    path('details/<str:title>/', sdetails_song, name="sdetails_song"),
    path('search/', ssearch_song, name="ssearch_song"),
    path('addsong/', sadd_song, name="sadd_song"),
    path('modifysong/<str:subject>/<str:title>', smodify_song, name="smodify_song"),
]
