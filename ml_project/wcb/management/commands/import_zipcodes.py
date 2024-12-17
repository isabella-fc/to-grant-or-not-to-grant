import csv
from django.core.management.base import BaseCommand
from wcb.models import NYZipCode
import os
from django.conf import settings

class Command(BaseCommand):
    help = "Import ZIP Codes and Frequencies from a CSV file"

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'data', 'zipcode_frequency_encoder.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(f"CSV file not found at {csv_path}")
            return

        # Clear existing data
        self.stdout.write("Deleting all existing NYZipCode data...")
        NYZipCode.objects.all().delete()

        # Import data
        self.stdout.write("Importing data from CSV...")
        with open(csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                carrier_name = row['ZipCode']
                frequency = float(row['ZipCode_Frequency'])

                NYZipCode.objects.create(zip_code=zip_code, encoded_value=frequency)

        self.stdout.write(self.style.SUCCESS("Import completed successfully!"))
