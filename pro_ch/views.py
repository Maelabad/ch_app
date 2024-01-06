
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def acceuil(request):
    if request.method == 'POST':
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
            # Authentification échouée
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    # Récupérez les messages après la logique conditionnelle du formulaire
    django_messages = [str(message) for message in messages.get_messages(request)]

    # Ajoutez les messages à votre contexte
    context = {
        'django_messages': django_messages,
    }

    return render(request, "acceuil.html", context)
