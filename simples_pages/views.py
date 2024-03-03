import requests
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from requests.exceptions import ConnectionError
    

def get_list(request):
    
    data = None
    retries = 3
    for attempt in range(retries):
        try:
            # api_url_list = correspond a l'affichage de la liste de chansons a partir de l'API
            api_url_list = "https://api-ch-4ujc.onrender.com"
            response = requests.get(api_url_list)
            if response.status_code == 200:
                data = response.json()
        except ConnectionError as e:
            print(f"Connection error occurred: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                continue
            else:
                print("Max retries exceeded.")
                raise  # Re-raise the exception if max retries exceeded

    return render(request, "index.html", {"data":data})



def details_song(request, title):
    # api_url_details = correspond a l'affichage d'une chanson a partir de l'API

    data = None
    retries = 3
    for attempt in range(retries):
        try:
            # api_url_list = correspond a l'affichage de la liste de chansons a partir de l'API
            api_url_details = f"https://api-ch-4ujc.onrender.com/details_song/{title}"
            response = requests.get(api_url_details)
            if response.status_code == 200:
                data = response.json()
        except ConnectionError as e:
            print(f"Connection error occurred: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                continue
            else:
                print("Max retries exceeded.")
                raise  # Re-raise the exception if max retries exceeded
    return render(request, "details_song.html", {"data":data})
    


def search_song(request):
    
    data = None
    retries = 3
    for attempt in range(retries):
        try:
            # api_url_details = correspond a l'affichage d'une chanson a partir de l'
            query = request.GET.get('query', '')  # Obtenez la valeur du paramètre query
            api_url_search = f"https://api-ch-4ujc.onrender.com/search_songs/{query}"
            response = requests.get(api_url_search)

            if response.status_code == 200:
                data = response.json()
        except ConnectionError as e:
            print(f"Connection error occurred: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                continue
            else:
                print("Max retries exceeded.")
                raise  # Re-raise the exception if max retries exceeded
    
    return render(request, "search_results.html", {"data": data})

