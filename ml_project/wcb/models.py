from django.db import models
from django.utils import timezone
# Create your models here.

class ClaimPrediction(models.Model):
    accident_date = models.DateField()
    c2_date = models.DateField()
    age_at_injury = models.IntegerField()
    assembly_date = models.DateField()
    average_weekly_wage = models.CharField(max_length=20)
    birth_year = models.IntegerField()
    ime4_count = models.IntegerField()
    number_of_dependents = models.IntegerField()
    attorney_representative = models.BooleanField()
    covid_indicator = models.BooleanField()
    c3_form_submitted = models.BooleanField()
    first_hearing_date = models.BooleanField()
    alternative_dispute_resolution = models.BooleanField()
    carrier_type = models.CharField(max_length=100)
    gender = models.CharField(max_length=1)
    district_name = models.CharField(max_length=100)
    medical_fee_region = models.CharField(max_length=100)
    county_of_injury = models.CharField(max_length=100)
    industry_code = models.CharField(max_length=10)
    wcio_cause_of_injury_code = models.CharField(max_length=10)
    wcio_nature_of_injury_code = models.CharField(max_length=10)
    wcio_part_of_body_code = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)
    carrier_name = models.CharField(max_length=200)
    claim_injury_type = models.CharField(max_length=200)
    run_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim Prediction ({self.id})"

class NYZipCode(models.Model):
    zip_code = models.CharField(max_length=5, unique=True)
    encoded_value = models.FloatField(default=0.0)  # Zip code frequency as a float

    def __str__(self):
        return f"{self.zip_code} - {self.encoded_value}"


class CarrierName(models.Model):
    carrier_name = models.CharField(max_length=100)
    encoded_value = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.carrier_name} - {self.encoded_value}"


