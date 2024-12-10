import os
from django.shortcuts import render
from django.conf import settings
from .models import Predictions
from .forms import ModelForm
import pickle

def predict_model(request):
    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            sepal_length = form.cleaned_data['sepal_length']
            sepal_width = form.cleaned_data['sepal_width']
            petal_length = form.cleaned_data['petal_length']
            petal_width = form.cleaned_data['petal_width']

            model_features = [[sepal_length, sepal_width, petal_length, petal_width]]

            # Construct the model path
            model_path = os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'wcb_model.pkl')
            print(f"Resolved model path: {model_path}")  # Debugging

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at: {model_path}")

            with open(model_path, 'rb') as model_file:
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

            return render(request, 'home.html', {'form': form, 'prediction': prediction_name})

    else:
        form = ModelForm()

    return render(request, 'home.html', {'form': form})
