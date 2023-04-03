from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
from django.conf import settings



class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "Buyer"),
        (2, "Seller"),
        (3, "Admin"),
    )

    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    email_token = models.CharField(max_length=255, default=uuid.uuid4())
    is_verfied = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name != "" and self.last_name != "":
            return self.first_name + " " + self.last_name
        else:
            return self.email
        

class UserLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    province = models.CharField(max_length=155)
    district = models.CharField(max_length=155)
    sector = models.CharField(max_length=155)
    cell = models.CharField(max_length=155)
    village = models.CharField(max_length=155)

    def __str__(self):
        return self.user.email


class UserAvatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', default='default_avatar.png')

    def __str__(self):
        return self.user.email