# from django.db import models
# Build a JSON REST API with CRUD operations for Provider (name, email, phone number, language an currency) and ServiceArea (name, price, geojson information)
from django.contrib.gis.db import models
from django.core.validators import RegexValidator


class Provider(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=250, validators=[
        RegexValidator(regex=r'^\+?\d{8,17}$', message='Non-valid Phone Number'),])
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    area = models.PolygonField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='providers')

    def __str__(self):
        return self.name

