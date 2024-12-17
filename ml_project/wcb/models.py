from django.db import models
from django.utils import timezone
# Create your models here.

class Predictions(models.Model):
    # The possible predictions the model can make in the 'predictions' field
    # defined by: (<database name>, <human readible name>)
    PREDICT_OPTIONS = [
        ('setosa', 'Setosa'),
        ('versicolor', 'Versicolor'),
        ('virginica', 'Virginica')
    ]

    # Prediction table fields (or columns) are defined by creating attributes
    # and assigning them to field instances such as models.CharField()
    predict_datetime = models.DateTimeField(default=timezone.now)
    sepal_length = models.DecimalField(decimal_places=2, max_digits=3)
    sepal_width = models.DecimalField(decimal_places=2, max_digits=3)
    petal_length = models.DecimalField(decimal_places=2, max_digits=3)
    petal_width = models.DecimalField(decimal_places=2, max_digits=3)
    prediction = models.CharField(choices=PREDICT_OPTIONS, max_length=10)

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


