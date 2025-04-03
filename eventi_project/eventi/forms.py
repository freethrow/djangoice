from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper

from crispy_forms.layout import (
    Layout,
    Fieldset,
    ButtonHolder,
    Submit,
    Row,
    Column,
    Div,
    HTML,
)
from .models import Event, EventFile


class EventFileForm(forms.ModelForm):
    class Meta:
        model = EventFile
        fields = ["file", "title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class EventForm(forms.ModelForm):
    file = forms.FileField(
        label=_("Documento"),
        required=False,
        help_text=_("Carica un file (docx, pdf, xlsx)"),
        widget=forms.ClearableFileInput(attrs={"class": "block w-full"}),
    )

    class Meta:
        model = Event
        fields = [
            "categoria",
            "office",
            "titolo",
            "data_inizio",
            "data_fine",
            "paese",
            "citta",
            "settore",
            "tipologia",
            "descrizione",
            "public",
            "privatistica"
        ]
        widgets = {
            "data_inizio": forms.DateInput(attrs={"type": "date"}),
            "data_fine": forms.DateInput(attrs={"type": "date"}),
            "descrizione": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "public": _("Se selezionato, l'evento sarà visibile a tutti gli utenti"),
            "data_fine": _("Opzionale. Lasciare vuoto per eventi di un solo giorno"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"  # Important for file uploads
        self.helper.layout = Layout(
            Fieldset(
                _("Informazioni Generali"),
                Row(
                    Column("categoria", css_class="md:w-1/2 px-2"),
                    Column("office", css_class="md:w-1/2 px-2"),
                    css_class="flex flex-wrap -mx-2",
                ),
                "titolo",
            ),
            Fieldset(
                _("Date e Luogo"),
                Row(
                    Column("data_inizio", css_class="md:w-1/2 px-2"),
                    Column("data_fine", css_class="md:w-1/2 px-2"),
                    css_class="flex flex-wrap -mx-2",
                ),
                Row(
                    Column("paese", css_class="md:w-1/2 px-2"),
                    Column("citta", css_class="md:w-1/2 px-2"),
                    css_class="flex flex-wrap -mx-2",
                ),
            ),
            Fieldset(
                _("Dettagli"),
                Row(
                    Column("settore", css_class="md:w-1/2 px-2"),
                    Column("tipologia", css_class="md:w-1/2 px-2"),
                    css_class="flex flex-wrap -mx-2",
                ),
                "descrizione",
                "public",
                "privatistica",
            ),
            Fieldset(
                _("Documenti"),
                "files",
                Div(HTML('<div id="file-list" class="mt-4"></div>'), css_class="mb-4"),
            ),
            ButtonHolder(
                HTML(
                    '<a class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 mr-2" href="{% url \'event_list\' %}">Annulla</a>'
                ),
                Submit(
                    "submit",
                    "Salva",
                    css_class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600",
                ),
                css_class="flex justify-between",
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        data_inizio = cleaned_data.get("data_inizio")
        data_fine = cleaned_data.get("data_fine")

        # Validate that end date is not before start date
        if data_inizio and data_fine and data_fine < data_inizio:
            self.add_error(
                "data_fine",
                _("La data di fine non può essere precedente alla data di inizio"),
            )

        return cleaned_data
