from django.shortcuts import render
import requests
from django.shortcuts import render

# Create your views here.
def get_list(request):
    # api_url_list = correspond a l'affichage de la liste de chansons a partir de l'API
    api_url_list = "https://api-ch-4ujc.onrender.com"
    response = requests.get(api_url_list)
    if response.status_code == 200:
        data = response.json()

    else:
        data = None
    return render(request, "index.html", {"data":data})

"""
A part la premiere view les autres ont besoins de parametres. Comment faire?
Interfacer Django avec mongoDB (ou pas). En effet la premiere page, nous renvoie une liste, avec url 
et tout. So we can get the params of a song in particular without search on the mongo database.
For the 3rd views il s'agirait de passer le mot clé (string) 

"""

def details_song(request, title):
    # api_url_details = correspond a l'affichage d'une chanson a partir de l'API
    
    api_url_details = f"https://api-ch-4ujc.onrender.com/details_song/{title}"
    response = requests.get(api_url_details)
    if response.status_code == 200:
        data = response.json()
        print("*"*40)
        print(data)
        print("*"*40)
    else:
        data = None
    return render(request, "details_song.html", {"data":data})
    


def search_song(request):
    # api_url_details = correspond a l'affichage d'une chanson a partir de l'
    query = request.GET.get('query', '')  # Obtenez la valeur du paramètre query
    api_url_search = f"https://api-ch-4ujc.onrender.com/search_songs/{query}"
    response = requests.get(api_url_search)
    if response.status_code == 200:
        data = response.json()
    else:
        data = None

    return render(request, "search_results.html", {"data": data})
