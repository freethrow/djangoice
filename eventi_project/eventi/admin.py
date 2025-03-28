# admin.py
from django.contrib import admin
from .models import Event, EventFile


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "titolo",
        "office",
        "data_inizio",
        "data_fine",
        "citta",
        "paese",
        "settore",
        "tipologia",
        "public",
    )
    list_filter = ("public", "categoria", "paese", "office", "settore", "tipologia")
    search_fields = ("titolo", "descrizione", "citta")
    date_hierarchy = "data_inizio"
    fieldsets = (
        (
            "Informazioni Generali",
            {"fields": ("categoria", "office", "titolo", "public")},
        ),
        ("Date", {"fields": ("data_inizio", "data_fine")}),
        ("Località", {"fields": ("paese", "citta")}),
        ("Categorizzazione", {"fields": ("settore", "tipologia")}),
        ("Dettagli", {"fields": ("descrizione",)}),
    )


admin.site.register(EventFile)
