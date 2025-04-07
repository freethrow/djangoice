import os
import io
from django.core import management
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventi_project.settings")
django.setup()


# Open file with explicit UTF-8 encoding
with io.open("eventi.json", "w", encoding="utf-8") as f:
    # Call the dumpdata command with the file as output
    management.call_command("dumpdata", "eventi", indent=2, stdout=f)

print("Data successfully exported to eventi.json with UTF-8 encoding")
