# admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Event, EventFile, Settore


@admin.register(Event)
class EventAdmin(ModelAdmin):
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



@admin.register(Settore)
class SettoreAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)


#admin.site.register(EventFile)

@admin.register(EventFile)
class EventFileAdmin(ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)
