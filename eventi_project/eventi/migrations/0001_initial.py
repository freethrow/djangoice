# Generated by Django 5.1.6 on 2025-02-28 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                (
                    "categoria",
                    models.CharField(max_length=255, verbose_name="Categoria"),
                ),
                (
                    "office",
                    models.CharField(
                        choices=[("Belgrado", "Belgrado"), ("Podgorica", "Podgorica")],
                        max_length=50,
                        verbose_name="Office",
                    ),
                ),
                ("titolo", models.CharField(max_length=255, verbose_name="Titolo")),
                ("data_inizio", models.DateField(verbose_name="Data Inizio")),
                (
                    "data_fine",
                    models.DateField(blank=True, null=True, verbose_name="Data Fine"),
                ),
                (
                    "paese",
                    models.CharField(
                        choices=[
                            ("Italia", "Italia"),
                            ("Serbia", "Serbia"),
                            ("Montenegro", "Montenegro"),
                        ],
                        max_length=50,
                        verbose_name="Paese",
                    ),
                ),
                ("citta", models.CharField(max_length=100, verbose_name="Città")),
                ("settore", models.CharField(max_length=255, verbose_name="Settore")),
                (
                    "tipologia",
                    models.CharField(max_length=255, verbose_name="Tipologia"),
                ),
                ("descrizione", models.TextField(verbose_name="Descrizione")),
                ("public", models.BooleanField(default=True, verbose_name="Public")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Data creazione"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Data aggiornamento"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="events_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creato da",
                    ),
                ),
                (
                    "last_updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="events_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ultimo aggiornamento da",
                    ),
                ),
            ],
            options={
                "verbose_name": "Evento",
                "verbose_name_plural": "Eventi",
                "ordering": ["-data_inizio"],
            },
        ),
    ]
