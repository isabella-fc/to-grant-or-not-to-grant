import csv
from django.core.management.base import BaseCommand
from wcb.models import NYZipCode
import os
from django.conf import settings


class Command(BaseCommand):
    help = "Import New York State ZIP Codes and County Names from CSV"

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'data',
                                'New_York_State_ZIP_Codes-County_FIPS_Cross-Reference_20241216.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(f"CSV file not found at {csv_path}")
            return

        with open(csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                zip_code = row['ZIP Code']
                county_name = row['County Name']

                NYZipCode.objects.get_or_create(zip_code=zip_code, county=county_name)

        self.stdout.write("Import completed successfully!")