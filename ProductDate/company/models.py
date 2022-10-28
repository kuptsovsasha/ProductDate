from django.db import models


class Company(models.Model):

    title = models.CharField(max_length=128)
    address = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)


class Shop(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
