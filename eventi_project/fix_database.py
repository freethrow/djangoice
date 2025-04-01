# Save this as fix_database.py and run it with python manage.py shell < fix_database.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventi_project.settings')
django.setup()

from django.db import connection
from eventi.models import Settore, Event

# Step 1: Check if the Settore model exists and create it if needed
print("Checking Settore model...")
if Settore.objects.count() == 0:
    # Create settore instances from the unique values
    unique_settori = [
        "Macchine agricole", "Occhialeria", "Calzature", "Agroalimentare",
        "Climatizzazione", "Cosmetica", "Editoria", "Vino", "Arredamento",
        "Macchine lavorazione legno", "Economia circolare", "Tessile",
        "Florovivaistico", "Macchine per calzature", "Alimentare",
        "Arredamento contract", "Metalmeccanica", "Macchine agricole e alimentari",
        "Metalmeccanico", "Mobili / Arredo", "Fitness", "Florovivaismo",
        "Gioielleria", "Food & Wine", "Marmo", "Plastica",
        "Officine, componentistica", "Plurisettoriale", "Turismo", "Nautico"
    ]
    for nome in unique_settori:
        Settore.objects.create(nome=nome)
    print(f"Created {len(unique_settori)} Settore instances")
else:
    print(f"Found {Settore.objects.count()} existing Settore instances")

# Step 2: Fix the database schema directly using SQL
print("\nChecking database schema...")
with connection.cursor() as cursor:
    # Check if the settore column exists
    cursor.execute("PRAGMA table_info(eventi_event)")
    columns = {column[1]: column for column in cursor.fetchall()}
    
    # Check if the needed columns exist
    has_old_settore = 'settore' in columns
    has_settore_id = 'settore_id' in columns
    
    print(f"Old 'settore' column exists: {has_old_settore}")
    print(f"Foreign key 'settore_id' column exists: {has_settore_id}")
    
    if not has_settore_id:
        print("\nCreating settore_id column...")
        cursor.execute("ALTER TABLE eventi_event ADD COLUMN settore_id integer REFERENCES eventi_settore(id)")
        print("Column created successfully")
    
    # Step 3: Migrate data from old settore field to new foreign key relationships
    if has_old_settore:
        print("\nMigrating data from settore text field to settore_id foreign key...")
        
        # Get all existing events with their settore values
        cursor.execute("SELECT id, settore FROM eventi_event")
        events_settori = cursor.fetchall()
        
        # Get all settore instances for mapping
        settore_map = {s.nome: s.id for s in Settore.objects.all()}
        print(f"Found {len(events_settori)} events to migrate")
        
        updated_count = 0
        default_settore_id = Settore.objects.first().id if Settore.objects.exists() else None
        
        for event_id, settore_nome in events_settori:
            # Try to find a matching settore (exact or partial match)
            settore_id = None
            
            # Exact match
            if settore_nome in settore_map:
                settore_id = settore_map[settore_nome]
            else:
                # Try partial match
                for nome, sid in settore_map.items():
                    if nome in settore_nome or settore_nome in nome:
                        settore_id = sid
                        break
            
            # Use default if no match
            if settore_id is None and default_settore_id:
                settore_id = default_settore_id
            
            if settore_id:
                cursor.execute("UPDATE eventi_event SET settore_id = ? WHERE id = ?", [settore_id, event_id])
                updated_count += 1
        
        print(f"Updated {updated_count} events with settore_id")
        
        # Remove old settore column (optional, comment this out if you want to keep it)
        # print("\nRemoving old settore column...")
        # Create a temporary table with the correct schema
        # cursor.execute("""
        # CREATE TEMPORARY TABLE eventi_event_new(
        #     id integer PRIMARY KEY,
        #     categoria varchar(255) NOT NULL,
        #     office varchar(50) NOT NULL,
        #     titolo varchar(255) NOT NULL,
        #     data_inizio date NOT NULL,
        #     data_fine date NULL,
        #     paese varchar(50) NOT NULL,
        #     citta varchar(100) NOT NULL,
        #     settore_id integer NULL REFERENCES eventi_settore(id),
        #     tipologia varchar(255) NOT NULL,
        #     descrizione text NOT NULL,
        #     public bool NOT NULL,
        #     created_by_id integer NULL,
        #     last_updated_by_id integer NULL,
        #     created_at datetime NOT NULL,
        #     updated_at datetime NOT NULL
        # )
        # """)
        # 
        # # Copy data without the old settore column
        # cursor.execute("""
        # INSERT INTO eventi_event_new 
        # SELECT id, categoria, office, titolo, data_inizio, data_fine, paese, citta, 
        #        settore_id, tipologia, descrizione, public, 
        #        created_by_id, last_updated_by_id, created_at, updated_at 
        # FROM eventi_event
        # """)
        # 
        # # Replace the tables
        # cursor.execute("DROP TABLE eventi_event")
        # cursor.execute("ALTER TABLE eventi_event_new RENAME TO eventi_event")
        # print("Old settore column removed")

print("\nDatabase update complete!")