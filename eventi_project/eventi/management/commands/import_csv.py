# eventi/management/commands/import_csv.py
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from eventi.models import Event

User = get_user_model()


class Command(BaseCommand):
    help = "Import events from the provided CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")
        parser.add_argument("--user", type=str, help="Username to attribute events to")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        username = options.get("user")

        # Get user if specified
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(f"Will attribute events to user: {username}")
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"User '{username}' not found. Continuing without user attribution."
                    )
                )

        # Read CSV and create events
        events_created = 0
        events_failed = 0

        with open(csv_file, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                try:
                    # Convert boolean string to actual boolean
                    if "public" in row:
                        row["public"] = row["public"].lower() in ["true", "1", "yes"]

                    # Create event object
                    event = Event(
                        categoria=row.get("categoria", ""),
                        office=row.get("office", "Belgrado"),
                        titolo=row.get("titolo", ""),
                        data_inizio=row.get("data_inizio", None),
                        data_fine=row.get("data_fine", None),
                        paese=row.get("paese", "Italia"),
                        citta=row.get("citta", ""),
                        settore=row.get("settore", ""),
                        tipologia=row.get("tipologia", ""),
                        descrizione=row.get("descrizione", ""),
                        public=row.get("public", True),
                        created_by=user,
                        last_updated_by=user,
                    )
                    event.save()
                    events_created += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error creating event: {str(e)}")
                    )
                    self.stdout.write(self.style.ERROR(f"Problematic row: {row}"))
                    events_failed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {events_created} events created, {events_failed} failed"
            )
        )
