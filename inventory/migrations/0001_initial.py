# Generated by Django 5.1.2 on 2025-07-16 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0011_alter_product_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="InventoryItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stock", models.IntegerField(default=0)),
                (
                    "barcode_value",
                    models.CharField(blank=True, max_length=32, unique=True),
                ),
                (
                    "barcode_image",
                    models.ImageField(blank=True, null=True, upload_to="barcodes/"),
                ),
                ("label_text", models.CharField(blank=True, max_length=128)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inventory_item",
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
