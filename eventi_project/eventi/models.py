from django.db import models
from django.conf import settings
from django.utils.text import slugify

from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage

import os

from .storage import BackblazeB2Storage


class Event(models.Model):
    COUNTRY_CHOICES = [
        ("Italia", "Italia"),
        ("Serbia", "Serbia"),
        ("Montenegro", "Montenegro"),
    ]

    OFFICE_CHOICES = [
        ("Belgrado", "Belgrado"),
        ("Podgorica", "Podgorica"),
    ]

    CATEGORIA_CHOICES = [
        (
            "Iniziative promozionali in Italia e all'estero",
            "Iniziative promozionali in Italia e all'estero",
        ),
        ("Iniziative promozionali in loco", "Iniziative promozionali in loco"),
    ]

    categoria = models.CharField("Categoria", max_length=255, choices=CATEGORIA_CHOICES)
    office = models.CharField("Office", max_length=50, choices=OFFICE_CHOICES)
    titolo = models.CharField("Titolo", max_length=255)
    data_inizio = models.DateField("Data Inizio")
    data_fine = models.DateField("Data Fine", blank=True, null=True)
    paese = models.CharField("Paese", max_length=50, choices=COUNTRY_CHOICES)
    citta = models.CharField("Città", max_length=100)
    settore = models.CharField("Settore", max_length=255)
    tipologia = models.CharField("Tipologia", max_length=255)
    descrizione = models.TextField("Descrizione")
    public = models.BooleanField("Public", default=True)

    # User tracking fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="events_created",
        verbose_name="Creato da",
    )
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="events_updated",
        verbose_name="Ultimo aggiornamento da",
    )

    # Timestamp fields
    created_at = models.DateTimeField("Data creazione", auto_now_add=True)
    updated_at = models.DateTimeField("Data aggiornamento", auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventi"
        ordering = ["-data_inizio"]

    def __str__(self):
        return f"{self.titolo} - {self.citta} ({self.data_inizio})"


def get_upload_path(instance, filename):
    """
    Generate a clean path for file uploads based on the related event
    Uses forward slashes and slugifies the filename to prevent path issues
    """
    # Get file extension
    ext = os.path.splitext(filename)[1].lower()

    # Slugify the base filename (remove special chars, spaces, etc.)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    safe_filename = slugify(base_name)[:50] + ext  # Limit filename length

    # Ensure forward slashes are used (for cross-platform compatibility)
    return f"event_files/{instance.event.id}/{safe_filename}"


class EventFile(models.Model):

    FILE_TYPE_CHOICES = [
        ("docx", "Word Document"),
        ("pdf", "PDF Document"),
        ("xlsx", "Excel Spreadsheet"),
    ]
    event = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Evento correlato",
    )
    file = models.FileField(
        "File",
        upload_to=get_upload_path,
        storage=BackblazeB2Storage(),
        max_length=255,  # Increase max_length for longer paths
    )
    title = models.CharField("Titolo del file", max_length=255)

    file_type = models.CharField(
        "Tipo di file", max_length=10, choices=FILE_TYPE_CHOICES, blank=True
    )
    description = models.TextField("Descrizione", blank=True)

    # User tracking fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="event_files_created",
        verbose_name="Caricato da",
    )

    # Timestamp fields
    created_at = models.DateTimeField("Data caricamento", auto_now_add=True)

    class Meta:
        verbose_name = "File Evento"
        verbose_name_plural = "File Eventi"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.event.titolo}"

    def save(self, *args, **kwargs):
        # Auto-detect file type from extension if not provided
        if not self.file_type:
            filename = self.file.name
            extension = os.path.splitext(filename)[1].lower().replace(".", "")
            if extension in [choice[0] for choice in self.FILE_TYPE_CHOICES]:
                self.file_type = extension
        super().save(*args, **kwargs)
