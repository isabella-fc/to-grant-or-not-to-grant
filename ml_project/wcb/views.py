
import matplotlib.pyplot as plt
from django.shortcuts import render

from .forms import ModelForm
from utils.ml_utils import *
import pickle
from wcb.models import NYZipCode, CarrierName, ClaimPrediction

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

            form_data = form.cleaned_data
            run_time = datetime.now()

            # Make prediction
            # Prepare model features from form data
            model_features = preprocess_form(form_data)

            # Make prediction
            prediction = loaded_model.predict(model_features)
            prediction_name = decode_prediction(prediction)

            # Save prediction to database
            ClaimPrediction.objects.create(
                accident_date=form_data.get('accident_date'),
                c2_date=form_data.get('c2_date'),
                age_at_injury=form_data.get('age_at_injury'),
                assembly_date=form_data.get('assembly_date'),
                average_weekly_wage=form_data.get('average_weekly_wage'),
                birth_year=form_data.get('birth_year'),
                ime4_count=form_data.get('ime4_count'),
                number_of_dependents=form_data.get('number_of_dependents'),
                attorney_representative=form_data.get('attorney_representative'),
                covid_indicator=form_data.get('covid_indicator'),
                c3_form_submitted=form_data.get('c3_form_submitted'),
                first_hearing_date=form_data.get('first_hearing_date'),
                alternative_dispute_resolution=form_data.get('alternative_dispute_resolution'),
                carrier_type=form_data.get('carrier_type'),
                gender=form_data.get('gender'),
                district_name=form_data.get('district_name'),
                medical_fee_region=form_data.get('medical_fee_region'),
                county_of_injury=form_data.get('county_of_injury'),
                industry_code=form_data.get('industry_code'),
                wcio_cause_of_injury_code=form_data.get('wcio_cause_of_injury_code'),
                wcio_nature_of_injury_code=form_data.get('wcio_nature_of_injury_code'),
                wcio_part_of_body_code=form_data.get('wcio_part_of_body_code'),
                zip_code=form_data.get('zip_code'),
                carrier_name=form_data.get('carrier_name'),
                claim_injury_type=prediction_name,
                run_time=run_time
            )

            return render(request, 'model_prediction.html', {
                'form': ModelForm(),
                'prediction': prediction_name,
                'feature_importance_plot': feature_importance_path,
                'zip_codes': zip_codes,
                'carrier_names': carrier_names,
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


