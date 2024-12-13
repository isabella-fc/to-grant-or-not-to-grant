import pandas as pd
import numpy as np
import os
import shap
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
from django.conf import settings
from sklearn.metrics import classification_report

from .models import Predictions
from .forms import ModelForm
import pickle

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'wcb_model.pkl')

def home(request):
    return render(request, 'index.html')


def model_prediction(request):
    shap_plot_path = os.path.join(settings.MEDIA_ROOT, 'shap_plot.png')
    feature_importance_path = os.path.join(settings.BASE_DIR, 'static', 'feature_importance.png')

    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            cleaned_data = form.cleaned_data

            # Prepare features in the correct order
            model_features = np.array([[
                cleaned_data['age_at_injury'],
                cleaned_data['average_weekly_wage'],
                cleaned_data['ime4_count'],
                cleaned_data['number_of_dependents'],
                1 if cleaned_data['attorney_representative'] == 'True' else 0,
                1 if cleaned_data['covid_indicator'] == 'True' else 0,
                1 if cleaned_data['carrier_type'] == '1A. PRIVATE' else
                2 if cleaned_data['carrier_type'] == '2A. SIF' else 3,  # Carrier Type encoding
                1 if cleaned_data['district_name'] == 'NYC' else 0,  # District encoding
                1 if cleaned_data['gender'] == 'M' else 0,  # Gender encoding
                1 if cleaned_data['medical_fee_region'] == 'IV' else 0,  # Medical Fee Region encoding
                cleaned_data['birth_year'],
                cleaned_data['carrier_name'],  # String input; ensure model supports string handling or encode it
                cleaned_data['county_of_injury'],
                cleaned_data['industry_code'],
                cleaned_data['wcio_cause_of_injury_code'],
                cleaned_data['wcio_nature_of_injury_code'],
                cleaned_data['wcio_part_of_body_code'],
                cleaned_data['zip_code'],
            ]])

            # Load model
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

            with open(MODEL_PATH, 'rb') as model_file:
                loaded_model = pickle.load(model_file)

            # Make prediction
            prediction = loaded_model.predict(model_features)[0]
            prediction_name = f"Class {prediction}"  # Customize based on your model's output classes

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

            plt.figure(figsize=(10, 6))
            plt.barh(features, importance)
            plt.xlabel('Feature Importance')
            plt.ylabel('Features')
            plt.title('Feature Importance Plot')
            plt.tight_layout()  # Prevent label overlap
            plt.savefig(feature_importance_path)
            plt.close()

            return render(request, 'model_prediction.html', {
                'form': form,
                'prediction': prediction_name,
                'feature_importance_plot': feature_importance_path,
            })

    else:
        form = ModelForm()

    return render(request, 'model_prediction.html', {'form': form})



def feature_importance(request):
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)

    importance = model.feature_importances_
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

    plt.bar(features, importance)
    plt.title('Feature Importance')
    plt.savefig(os.path.join(settings.BASE_DIR, 'static', 'feature_importance.png'))
    return render(request, 'feature_importance.html', {'plot': 'feature_importance.png'})


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

def data_summary(request):
    data = pd.read_csv(os.path.join(settings.BASE_DIR, 'data', 'train_data.csv'))
    summary = {
        'total_claims': str(len(data)),
        'covid_related': str(data['COVID-19 Indicator'].sum()),
        'avg_age': str(data['Age at Injury'].mean()),
    }
    return render(request, 'data_summary.html', {'summary': summary})