from django.db import models
from django_countries.fields import Country, CountryField
from django.contrib.auth import get_user_model, models as auth_models
from django.conf import settings
from ..core.permissions import StorePermissions

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=255)
    country = CountryField()
    # TODO: do we need to support different currency in store?
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='stores')

    class Meta:
        permissions = (
            (StorePermissions.MANAGE_STORES.codename, "Manage stores"),
        )
