# Upload files to differents databases (mongoDB, Cloudinary  and Backblaze)
import magic 
import os
import cloudinary
from pymongo import MongoClient
from cloudinary.uploader import upload
from pathlib import Path


mongo_client_pwd = os.getenv("MONGO_CLIENT_PWD")
client = MongoClient(f"mongodb+srv://sylvainhudson12724:{mongo_client_pwd}@cluster0.z9gjdsx.mongodb.net/?retryWrites=true&w=majority")


db = client.get_database("choir_song")

# Obtenez une référence à votre collection MongoDB
collection = db.get_collection("pdfs")


cloudinary.config( 
  cloud_name = os.getenv("CLOUD_NAME"), 
  api_key = os.getenv("API_KEY"), 
  api_secret = os.getenv("API_SECRET") 
)



def add_song_to_db(title, subject, url):
    """Add a song to the mongoDB"""

    # Vérifiez si la chanson existe déjà dans la collection
    existing_song = collection.find_one({"title": title})
    if existing_song:
        print("Cette chanson existe déjà dans la base de données")
        
    #    raise HTTPException(status_code=400, detail="Cette chanson existe déjà dans la base de données")

    # Ajoutez la nouvelle chanson à la collection
    collection.insert_one({"title": title, "subject": subject, "url": url})


def upload_files_to_DBs(file, title, subject):
    """Upload file to differents DBs"""

    dest_folder = 'choir'
    status = 0 #0 signifie rien n'a été fait, 1 le contraire
    try:
        
        # Utilisez la fonction `upload` pour uploader le PDF sur Cloudinary avec le nom du sujet comme sous-dossier
        result = upload(file, resource_type="raw", public_id=f"{dest_folder}/{os.path.splitext(file.name)[0]}")

        # Ajoutez le nom de fichier sans espaces ni extensions à la base de données
        nom_fichier_sans_extension = os.path.splitext(file.name)[0]  # Supprimer l'extension
        nom_fichier_sans_underscores = nom_fichier_sans_extension.replace("_", " ")  # Remplacer les underscores par des espaces
        add_song_to_db(nom_fichier_sans_underscores, subject, result['secure_url'])
        message = f"La chanson {file.name} a été ajouter avec succès."

    except Exception as e:
        message = f"Une erreur s'est produite lors de l'ajout de la chanson {file.name}."
    return message


def update_mongoDB_data(title, new_title, new_theme):
    # Recherche de l'élément avec le titre spécifique
    element_a_modifier = collection.find_one({'title': title})

    # Vérifier si l'élément a été trouvé
    if element_a_modifier:
        element_a_modifier['subject'] = new_theme
        element_a_modifier['title'] = new_title

        # Mettre à jour l'élément dans la base de données
        collection.update_one({'_id': element_a_modifier['_id']}, {'$set': element_a_modifier})
        
        # Faut aussi essayer de mettre a jour le nom du fichier sur cloudinary.
        # Est-ce possible de modifier le pdf en lui meme ? 
        
        
        message = f"""Les informations ont été mises à jour avec succès.\n 
                      Le titre est passé de {title} à {new_title}.\n
                      Le theme est devenu {new_theme}"""

    else:
        message = f"Une erreur s'est produite lors de la modification."

    return  message





