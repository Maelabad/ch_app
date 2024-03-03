from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self,username, password=None, user_type='user'):
        if not username:
            raise ValueError("Le champ 'username' est requis")
        
        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
            user_type='admin',
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def set_password(self, raw_password):
        """
        Modifie le mot de passe de l'utilisateur avec un mot de passe haché.
        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Vérifie si le mot de passe brut correspond au mot de passe haché stocké pour l'utilisateur.
        """
        return check_password(raw_password, self.password)