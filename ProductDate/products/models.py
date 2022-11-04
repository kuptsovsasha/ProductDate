from django.db import models

from ProductDate.company.models import Company, Shop


class Product(models.Model):
    class DepartmentChoices(models.TextChoices):
        DAIRY_PRODUCTS = "Dairy Products", "dairy_products"
        BEVERAGES = "Beverages", "beverages"
        BAKING_GOODS = "Baking Goods", "baking_goods"
        FROZEN_FOODS = "Frozen Foods", "frozen_foods"
        MEAT = "Meat", "meat"
        CLEANERS = "Cleaners", "cleaners"
        PAPER_GOODS = "Paper Goods", "paper_goods"
        PERSONAL_CARE = "Personal Care", "personal_care"
        OTHER = "Other", "other"

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, null=True, blank=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(
        max_length=50,
        choices=DepartmentChoices.choices,
        default=DepartmentChoices.OTHER,
    )
    expiration_date = models.DateField()
    is_exist = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
