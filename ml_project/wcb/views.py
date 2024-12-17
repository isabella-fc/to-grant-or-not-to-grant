import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
from .forms import ModelForm
from utils.ml_utils import *
import pickle
from django.http import JsonResponse
from dal import autocomplete
from wcb.models import NYZipCode, CarrierName

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'final_model.pkl')

def home(request):
    return render(request, 'index.html')


def model_prediction(request):
    feature_importance_path = os.path.join(settings.BASE_DIR, 'static', 'feature_importance.png')
    zip_codes = NYZipCode.objects.all().values('zip_code', 'encoded_value')
    carrier_names = CarrierName.objects.all().values('carrier_name', 'encoded_value')
    form = ModelForm(request.POST)

    if request.method == 'POST':


        if form.is_valid():

            # Load model
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

            with open(MODEL_PATH, 'rb') as model_file:
                loaded_model = pickle.load(model_file)

            # Make prediction
            # Prepare model features from form data
            model_features = preprocess_form(form.cleaned_data)

            # Make prediction
            prediction = loaded_model.predict(model_features)
            prediction_name = decode_prediction(prediction)

            # Generate feature importance plot
            importance = loaded_model.feature_importances_
            features = [
                'Age at Injury',
                'Average Weekly Wage',
                'IME-4 Count',
                'Number of Dependents',
                'Attorney Representative',
                'COVID Indicator',
                'Carrier Type',
                'District Name',
                'Gender',
                'Medical Fee Region',
                'Birth Year',
                'Carrier Name',
                'County of Injury',
                'Industry Code',
                'WCIO Cause of Injury Code',
                'WCIO Nature of Injury Code',
                'WCIO Part of Body Code',
                'Zip Code'
            ]

            return render(request, 'model_prediction.html', {
                'form': form,
                'prediction': prediction_name,
                'feature_importance_plot': feature_importance_path,
            })

    else:
        form = ModelForm()

    return render(request, 'model_prediction.html', {'form': form, 'zip_codes': zip_codes, 'carrier_names': carrier_names})



def feature_importance(request):
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)

    importance = model.feature_importances_
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

    plt.bar(features, importance)
    plt.title('Feature Importance')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'feature_importance.png'))
    return render(request, 'feature_importance.html', {'plot': 'feature_importance.png'})

def binary_prediction(request):

    return


#def model_performance(request):
#    with open(MODEL_PATH, 'rb') as model_file:
#        model = pickle.load(model_file)
#    test_data, test_labels = ...  # Load your test data
#    predictions = model.predict(test_data)
#    report = classification_report(test_labels, predictions, output_dict=True)
#
#    metrics = {
#        'accuracy': report['accuracy'],
#        'precision': report['weighted avg']['precision'],
#        'recall': report['weighted avg']['recall'],
#        'f1_score': report['weighted avg']['f1-score']
#    }
#    return render(request, 'model_performance.html', {'metrics': metrics})


class NYZipCodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return NYZipCode.objects.none()

        qs = NYZipCode.objects.all()

        # Filter the queryset based on user input
        if self.q:
            qs = qs.filter(zip_code__icontains=self.q)  # Search by partial match on zip_code
        return qs
