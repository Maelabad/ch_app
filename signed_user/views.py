import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import upload_files_to_DBs, update_mongoDB_data
from django.utils.text import slugify  # Utilisé pour créer un slug à partir du titre
from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.contrib import messages


import os

"""
import cloudinary
from pymongo import MongoClient

#load_dotenv()

# Connexion à la base de données MongoDB Atlas
mongo_client_pwd = os.getenv("MONGO_CLIENT_PWD")

client = MongoClient(f"mongodb+srv://sylvainhudson12724:{mongo_client_pwd}@cluster0.z9gjdsx.mongodb.net/?retryWrites=true&w=majority")


db = client.get_database("choir")

# Obtenez une référence à votre collection MongoDB
collection = db.get_collection("pdfs")


cloudinary.config( 
  cloud_name = os.getenv("CLOUD_NAME"), 
  api_key = os.getenv("API_KEY"), 
  api_secret = os.getenv("API_SECRET") 
)
"""

def authentication(request):
    messages.error(request, "")
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        

        # Vérification des informations d'authentification
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentification réussie
            login(request, user)
            # Redirection après une connexion réussie
            return redirect('sget_list')
        else:
            print(username, password)
            # Authentification échouée
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, "authentication.html")




# Create your views here.
#@login_required
def sget_list(request):
    
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

    return render(request, "list_song_signed.html", {"data":data})

#@login_required
def sdetails_song(request, title):
    
    data = None
    retries = 3
    for attempt in range(retries):
        try:
            # api_url_details = correspond a l'affichage d'une chanson a partir de l'API
            
            directory = title
            
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
        
    return render(request, "details_song_signed.html", {"data":data})
    

#@login_required
def ssearch_song(request):
    
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
    
    return render(request, "search_results_signed.html", {"data": data})


#@login_required
def sadd_song(request):
    
    retries =3
    for attempt in range(retries):
        try:
            
        
            api_url_details = f"https://api-ch-4ujc.onrender.com/themes"
            themes = requests.get(api_url_details)
            
            if themes.status_code == 200:
                list_themes = themes.json()
            else:
                list_themes = None

            if request.method == 'POST':
                title = request.POST.get('title')
                theme = request.POST.get('themeChanson')
                pdf_file = request.FILES.get('pdfChanson')
                        
                slug = slugify(title)

                original_filename, file_extension = os.path.splitext(pdf_file.name)
                new_filename = f"{slug}{file_extension}"
                pdf_file.name = new_filename
                
                response = upload_files_to_DBs(pdf_file, title, theme)
                
                # Retourner a la page principale avec avec un message    
                return redirect(reverse('sget_list')  + '?message={}'.format(response))

        except ConnectionError as e:
            print(f"Connection error occurred: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                continue
            else:
                print("Max retries exceeded.")
                raise  # Re-raise the exception if max retries exceeded
        
    return render(request, 'ajouter.html', {"themes": list_themes})
        

#@login_required
def smodify_song(request, title, subject):
        
    if request.method == 'POST':

        #passer le sujet en parametre peut etre c'est ca l'option la plus simple
        # En tout cas il faut recuperer le subject pour faire la comparaison

        new_title = request.POST.get('titreChanson')
        new_theme = request.POST.get('themeChanson')
        
        if new_theme == 'default':
            new_theme = subject
        if new_title == 'default':
            new_title = title
        
        response = update_mongoDB_data(title, new_title, new_theme)
        
        return redirect(reverse('sget_list')  + '?message={}'.format(response))
        
    directory = title
    
    retries = 3
    for attempt in range(retries):
        try:
            
            # Recuperer les differents themes
            api_url_details = f"https://api-ch-4ujc.onrender.com/themes"
            themes = requests.get(api_url_details)
            
            if themes.status_code == 200:
                list_themes = themes.json()
                
                
            api_url_details = f"https://api-ch-4ujc.onrender.com/details_song/{title}"
            response = requests.get(api_url_details)
            
            if response.status_code == 200:
                data = response.json()
            else:
                data = None
        except ConnectionError as e:
            print(f"Connection error occurred: {e}")
            if attempt < retries - 1:
                print("Retrying...")
                continue
            else:
                print("Max retries exceeded.")
                data = None
                list_themes = None
                raise  # Re-raise the exception if max retries exceeded
            
    return render(request, 'modifier.html', {"data": data, "themes": list_themes} )