from django.shortcuts import render
from .models import Predictions
from .forms import ModelForm
import pickle

def predict_model(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            sepal_length = form.cleaned_data['sepal_length']
            sepal_width = form.cleaned_data['sepal_width']
            petal_length = form.cleaned_data['petal_length']
            petal_width = form.cleaned_data['petal_width']

            # Run new features through ML model
            model_features = [
                [sepal_length, sepal_width, petal_length, petal_width]]
                
            loaded_model = pickle.load(
                open("ml_project\ml_model\wcb_model.pkl", 'rb'))
            prediction = loaded_model.predict(model_features)[0]

            prediction_name_list = ['setosa', 'versicolor', 'virginica']

            prediction_name = prediction_name_list[prediction]

            Predictions.objects.create(sepal_length=sepal_length,
                            sepal_width=sepal_width,
                            petal_length=petal_length,
                            petal_width=petal_width,
                            prediction=prediction_name)

            return render(request, 'home.html', {'form': form, 'prediction': prediction_name})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ModelForm()

    return render(request, 'home.html', {'form': form})