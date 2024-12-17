import os
import pickle
from django.conf import settings

import pandas as pd
import numpy as np

from utils.lists import FEATURE_ORDER, COUNTIES

import pandas as pd
import numpy as np

from datetime import datetime

def preprocess_form(form_data):
    """
    Preprocess form.cleaned_data for XGBoost prediction:
    - Converts all string inputs into appropriate numeric types.
    - Converts categorical variables into numerical values.
    - Ensures strict column order according to FEATURE_ORDER.
    """
    # Helper functions
    def parse_boolean(value):
        return 1 if str(value).lower() == 'true' else 0 if str(value).lower() == 'false' else np.nan

    def parse_date(value):
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except (ValueError, TypeError):
            return None

    # Initialize processed_data with default values (0 or np.nan)
    processed_data = {feature: 0 for feature in FEATURE_ORDER}

    # Numeric fields
    numeric_fields = ['age_at_injury', 'average_weekly_wage', 'birth_year', 'ime4_count', 'number_of_dependents']
    for field in numeric_fields:
        processed_data[field.replace('_', ' ').title()] = float(form_data.get(field, 0))

    # Date fields
    date_fields = {
        'accident_date': 'Accident Date',
        'assembly_date': 'Assembly Date',
        'c2_date': 'C-2 Date'
    }
    for key, prefix in date_fields.items():
        date_value = parse_date(form_data.get(key, ""))
        if date_value:
            processed_data[f'{prefix}_Year'] = date_value.year
            processed_data[f'{prefix}_Month'] = date_value.month
            processed_data[f'{prefix}_Day'] = date_value.day
            processed_data[f'{prefix}_DayOfWeek'] = date_value.weekday()

    # Boolean fields
    boolean_fields = {
        'attorney_representative': 'Attorney/Representative',
        'covid_indicator': 'COVID-19 Indicator',
        'c3_form_submitted': 'C3 Form Submitted',
        'first_hearing_date': 'First Hearing Date',
        'alternative_dispute_resolution': 'Alternative Dispute Resolution',
        'medical_fee_region': 'Medical Fee Region'
    }
    for key, prefix in boolean_fields.items():
        processed_data[prefix] = parse_boolean(form_data.get(key))

    # Carrier Type mapping
    carrier_types = [
        '1A. PRIVATE', '2A. SIF', '3A. SELF PUBLIC', '4A. SELF PRIVATE',
        '5A. SPECIAL FUND - CONS. COMM. (SECT. 25-A)', 'UNKNOWN'
    ]
    carrier = form_data.get('carrier_type', 'UNKNOWN')
    for ct in carrier_types:
        processed_data[f'Carrier Type_{ct}'] = int(carrier == ct)

    # Gender mapping
    gender_mapping = ['F', 'M', 'U', 'X']
    gender = form_data.get('gender', 'U')
    for g in gender_mapping:
        processed_data[f'Gender_{g}'] = int(gender == g)

    # County mapping
    all_counties = ['ALBANY', 'BRONX', 'BROOME', 'DELAWARE', 'KINGS', 'UNKNOWN']  # Add all counties here
    county = form_data.get('county_of_injury', 'UNKNOWN')
    for c in all_counties:
        processed_data[f'County of Injury_{c}'] = int(county == c)

    # Text fields as placeholders
    text_fields = ['industry_code',
                   'wcio_cause_of_injury_code', 'wcio_nature_of_injury_code', 'wcio_part_of_body_code']
    for field in text_fields:
        processed_data[field.title().replace('_', ' ')] = int(form_data.get(field, 0))


    processed_data['Carrier Name'] = float(form_data.get('encoded_value_carrier', 0))
    processed_data['Zip Code'] = float(form_data.get('encoded_value', 0))

    # Create DataFrame and strictly enforce FEATURE_ORDER
    processed_df = pd.DataFrame([processed_data])

    # Drop unexpected columns
    processed_df = processed_df[[col for col in FEATURE_ORDER if col in processed_df.columns]]

    return processed_df

def decode_prediction(prediction):
    """
    Decodes the model prediction into a readable format.
    """

    # open label encoder
    with (open(os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'label_encoder.pkl'), 'rb')
          as le_file): label_encoder = pickle.load(le_file)

    return label_encoder.inverse_transform(prediction)
