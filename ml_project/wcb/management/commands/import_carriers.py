import csv
from django.core.management.base import BaseCommand
from wcb.models import CarrierName
import os
from django.conf import settings

class Command(BaseCommand):
    help = "Import CarrierName and Frequencies from a CSV file"

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'data', 'carrier_frequency_encoder.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(f"CSV file not found at {csv_path}")
            return

        # Clear existing data
        self.stdout.write("Deleting all existing CarrierName data...")
        CarrierName.objects.all().delete()

        # Import data
        self.stdout.write("Importing data from CSV...")
        with open(csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                carrier_name = row['CarrierName']
                frequency = float(row['CarrierName_Frequency'])

                CarrierName.objects.create(carrier_name=carrier_name, encoded_value=frequency)

        self.stdout.write(self.style.SUCCESS("Import completed successfully!"))
