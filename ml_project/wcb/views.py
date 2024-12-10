import os
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
from sklearn.metrics import classification_report

from .models import Predictions
from .forms import ModelForm
import pickle

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'wcb_model.pkl')

def home(request):
    return render(request, 'home.html')
def model_prediction(request):
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            sepal_length = form.cleaned_data['sepal_length']
            sepal_width = form.cleaned_data['sepal_width']
            petal_length = form.cleaned_data['petal_length']
            petal_width = form.cleaned_data['petal_width']

            model_features = [[sepal_length, sepal_width, petal_length, petal_width]]

            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

            with open(MODEL_PATH, 'rb') as model_file:
                loaded_model = pickle.load(model_file)

            prediction = loaded_model.predict(model_features)[0]
            prediction_name_list = ['setosa', 'versicolor', 'virginica']
            prediction_name = prediction_name_list[prediction]

            Predictions.objects.create(
                sepal_length=sepal_length,
                sepal_width=sepal_width,
                petal_length=petal_length,
                petal_width=petal_width,
                prediction=prediction_name
            )

            return render(request, 'model_prediction.html', {'form': form, 'prediction': prediction_name})

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
    plt.savefig(os.path.join(settings.BASE_DIR, 'staticfiles', 'feature_importance.png'))
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