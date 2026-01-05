from django.contrib.auth.models import AbstractUser
from django.db import models
import pycountry

EU_COUNTRY_CODES = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']
COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]

class CustomUser(AbstractUser):
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='PL')
    picture = models.ImageField(
    upload_to='profile_pics/',
        blank=True,
        null=True
    )



    def is_in_eu(self):
        return self.country in EU_COUNTRY_CODES

    def get_country_name(self):
        return dict(COUNTRY_CHOICES).get(self.country, '')

    def __str__(self):
        return self.username