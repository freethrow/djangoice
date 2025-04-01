from django.db import migrations, models


def create_settori_and_migrate_events(apps, schema_editor):
    """
    Create Settore instances and migrate existing Event records
    """
    # Get model classes
    Settore = apps.get_model('eventi', 'Settore')
    Event = apps.get_model('eventi', 'Event')

    # Unique sectors from the original list
    unique_settori = [
        "Macchine agricole",
        "Occhialeria",
        "Calzature",
        "Agroalimentare",
        "Climatizzazione",
        "Cosmetica",
        "Editoria",
        "Vino",
        "Arredamento",
        "Macchine lavorazione legno",
        "Economia circolare",
        "Tessile",
        "Florovivaistico",
        "Macchine per calzature",
        "Alimentare",
        "Arredamento contract",
        "Metalmeccanica",
        "Macchine agricole e alimentari",
        "Metalmeccanico",
        "Mobili / Arredo",
        "Fitness",
        "Florovivaismo",
        "Gioielleria",
        "Food & Wine",
        "Marmo",
        "Plastica",
        "Officine, componentistica",
        "Plurisettoriale",
        "Turismo",
        "Nautico",
    ]

    # Create Settore instances
    settore_instances = {}
    for nome in unique_settori:
        settore, created = Settore.objects.get_or_create(nome=nome)
        settore_instances[nome] = settore

    # Migrate existing events
    for event in Event.objects.all():
        # Find the corresponding Settore instance that matches the current event.settore string
        settore_nome = event.settore
        settore_instance = None
        
        # Direct match
        if settore_nome in settore_instances:
            settore_instance = settore_instances[settore_nome]
        else:
            # Try to find the closest match
            for nome in unique_settori:
                if nome in settore_nome or settore_nome in nome:
                    settore_instance = settore_instances[nome]
                    break
        
        # Use the first settore as fallback if no match found
        if not settore_instance and unique_settori:
            settore_instance = settore_instances[unique_settori[0]]
            
        # Update the event with the new foreign key
        if settore_instance:
            event.settore_new = settore_instance
            event.save(update_fields=['settore_new'])


class Migration(migrations.Migration):
    dependencies = [
        ('eventi', '0005_settore'),  # Update this to match your previous migration
    ]

    operations = [
        # Add a temporary field to store the foreign key
        migrations.AddField(
            model_name='event',
            name='settore_new',
            field=models.ForeignKey(
                null=True,
                on_delete=models.SET_NULL,
                related_name='events',
                to='eventi.Settore',
                verbose_name='Settore'
            ),
        ),
        
        # Run the data migration
        migrations.RunPython(create_settori_and_migrate_events),
        
        # Remove the old settore field
        migrations.RemoveField(
            model_name='event',
            name='settore',
        ),
        
        # Rename the new field to settore
        migrations.RenameField(
            model_name='event',
            old_name='settore_new',
            new_name='settore',
        ),
    ]