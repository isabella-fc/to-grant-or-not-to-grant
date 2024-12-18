import os
import pickle
from django.conf import settings

from utils.lists import FEATURE_ORDER, COUNTIES, INDUSTRY_CODES, CAUSE_OF_INJURY_CODES, NATURE_OF_INJURY_CODES, \
    PART_OF_BODY_CODES

import pandas as pd
import numpy as np

from datetime import datetime

import pandas as pd
import numpy as np


def preprocess_form(form_data):
    print(form_data)
    """
    Preprocess form.cleaned_data for XGBoost prediction:
    - Converts all string inputs into appropriate numeric types.
    - Converts categorical variables into numerical values.
    - Ensures strict column order according to FEATURE_ORDER.
    """

    numeric_features = ['Age at Injury', 'Average Weekly Wage', 'Birth Year', 'IME-4 Count', 'Number of Dependents']

    # Initialize processed_data with default values (0 or np.nan)
    processed_data = {feature: 0 for feature in FEATURE_ORDER}

    # Numeric fields
    processed_data['Age at Injury'] = form_data.get('age_at_injury', np.nan)
    processed_data['Average Weekly Wage'] = float(form_data.get('average_weekly_wage', np.nan))
    processed_data['Birth Year'] = form_data.get('birth_year', np.nan)
    ime4count = form_data.get('ime4_count', 0)
    processed_data['IME-4 Count'] = ime4count != 0
    processed_data['Number of Dependents'] = form_data.get('number_of_dependents', 0)

    # Date fields
    for field, prefix in {
        'accident_date': 'Accident Date_',
        'c2_date': 'C-2 Date_',
        'assembly_date': 'Assembly Date_',
    }.items():
        date_value = form_data.get(field, None)
        print(f"Processing date field: {field}, Value: {date_value}, Type: {type(date_value)}")  # Debugging
        processed_data = add_datetime_features(processed_data, date_value, prefix)

    # Boolean fields
    boolean_fields = {
        'covid_indicator': 'COVID-19 Indicator',
        'c3_form_submitted': 'Has C-3 Date',
        'first_hearing_date': 'Has First Hearing Date',
    }

    # Process boolean fields (idk why)
    for key, prefix in boolean_fields.items():
        field_value = form_data.get(key)
        processed_data = add_boolean_one_hot(processed_data, field_value, prefix)

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

    # Alternative dispute resolution mapping
    adr_options = {'False': 'N', 'True': 'Y', 'None': 'U'}
    for key, value in adr_options.items():
        processed_data[f'Alternative Dispute Resolution_{value}'] = int(
            form_data.get('alternative_dispute_resolution', 'U') == key)

    # representative and attorney mapping
    attorney_options = {'False': 'N', 'True': 'Y', }
    for key, value in attorney_options.items():
        processed_data[f'Attorney/Representative_{value}'] = int(
            form_data.get('attorney_representative', 'False') == key)

    # covid 19 indicator
    covid_options = {'False': 'N', 'True': 'Y', }
    for key, value in covid_options.items():
        processed_data[f'COVID-19 Indicator_{value}'] = int(form_data.get('covid_indicator', 'False') == key)

    medical_options = ['Medical Fee Region_I', "Medical Fee Region_II", "Medical Fee Region_III",
                       "Medical Fee Region_IV""Medical Fee Region_UK"]
    for option in medical_options:
        processed_data[option] = int(form_data.get('medical_fee_region', 'Medical Fee Region_UK') == option)

    # County mapping
    processed_data = match_one_hot_encoding(
        processed_data, COUNTIES, form_data.get('county_of_injury', 'UNKNOWN'), 'County of Injury_'
    )

    processed_data = match_one_hot_encoding(
        processed_data, INDUSTRY_CODES, form_data.get('industry_code', 'UNKNOWN'), 'Industry Code_',
        float_conversion=True
    )

    processed_data = match_one_hot_encoding(
        processed_data, CAUSE_OF_INJURY_CODES, form_data.get('wcio_cause_of_injury_code', 'UNKNOWN'),
        'WCIO Cause of Injury Code_', float_conversion=True
    )

    processed_data = match_one_hot_encoding(
        processed_data, NATURE_OF_INJURY_CODES, form_data.get('wcio_nature_of_injury_code', 'UNKNOWN'),
        'WCIO Nature of Injury Code_', float_conversion=True
    )

    processed_data = match_one_hot_encoding(
        processed_data, PART_OF_BODY_CODES, form_data.get('wcio_part_of_body_code', 'UNKNOWN'),
        'WCIO Part Of Body Code_', float_conversion=True
    )

    district_options = ['District Name_ALBANY', 'District Name_BINGHAMTON', 'District Name_BUFFALO',
                        'District Name_HAUPPAUGE', 'District Name_NYC', 'District Name_ROCHESTER',
                        'District Name_STATEWIDE', 'District Name_SYRACUSE', ]
    processed_data = match_one_hot_encoding(processed_data, district_options, form_data.get('district_name', 'UNKNOWN'),
                                            'District Name_')

    processed_data['Carrier Name'] = float(form_data.get('encoded_value_carrier', 0))
    processed_data['Zip Code'] = float(form_data.get('encoded_value', 0))

    # Create DataFrame and strictly enforce FEATURE_ORDER
    processed_df = pd.DataFrame([processed_data])

    # Drop unexpected columns
    processed_df = processed_df[[col for col in FEATURE_ORDER if col in processed_df.columns]]

    # Open Robust Scaler
    with (open(os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'scaler.pkl'), 'rb')
          as scaler_file):
        scaler = pickle.load(scaler_file)

    df_numeric = processed_df[numeric_features]

    # Apply scaling
    scaled_features = scaler.transform(df_numeric)

    # Replace scaled features in the original DataFrame
    scaled_df = pd.DataFrame(scaled_features, columns=numeric_features, index=processed_df.index)
    processed_df.update(scaled_df)

    processed_df[numeric_features] = processed_df[numeric_features].astype(float)

    # Replace 0 with NaN selectively
    columns_to_replace = [
        col for col in processed_df.select_dtypes(include=['int', 'float']).columns
        if '_' not in col
    ]

    return processed_df


def match_one_hot_encoding(df, features, value, prefix, float_conversion=False):
    """
    Matches the first value in a one-hot encoded feature set
    Leaves the rest 0
    """
    if float_conversion:
        value = float(value)

    for feature in features:
        # Check if the feature starts with the given prefix
        if feature.startswith(prefix):
            # Set the column to 1 if it matches the target value, otherwise 0
            df[feature] = 1 if feature == f"{prefix}{value}" else 0

    return df


def add_datetime_features(df, date_value, prefix):
    """
    Adds year, month, day, and day of the week features for a given date to the DataFrame.

    Args:
        df (dict): The dictionary to update with new features.
        date_value (datetime.date or str): The date value to extract features from.
        prefix (str): The prefix for the new feature names.

    Returns:
        dict: The updated dictionary with the new date-related features.
    """
    # Convert the date_value to pandas datetime if it's not None
    date_value = pd.to_datetime(date_value, errors='coerce')  # Handles None and invalid dates
    if pd.notnull(date_value):
        df[f'{prefix}Year'] = date_value.year
        df[f'{prefix}Month'] = date_value.month
        df[f'{prefix}Day'] = date_value.day
        df[f'{prefix}DayOfWeek'] = date_value.dayofweek
    else:
        # Assign NaN if the date is missing or invalid
        df[f'{prefix}Year'] = np.nan
        df[f'{prefix}Month'] = np.nan
        df[f'{prefix}Day'] = np.nan
        df[f'{prefix}DayOfWeek'] = np.nan

    return df


def add_boolean_one_hot(df, field_value, prefix):
    """
    Adds one-hot encoded columns for a boolean field to the DataFrame.

    Args:
        df (dict): The dictionary to update with new features.
        field_value (str or bool): The field value ('True', 'False', or equivalent).
        prefix (str): The prefix for the new one-hot encoded column names.

    Returns:
        dict: The updated dictionary with one-hot encoded columns.
    """
    # Parse the field value to determine boolean state
    parsed_value = 1 if str(field_value).lower() == 'true' else 0

    # Add one-hot encoded columns
    df[f'{prefix}_1'] = parsed_value
    df[f'{prefix}_0'] = 1 - parsed_value

    return df


def decode_prediction(prediction):
    """
    Decodes the model prediction into a readable format.
    """

    # open label encoder
    with (open(os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'label_encoder.pkl'), 'rb')
          as le_file): label_encoder = pickle.load(le_file)

    return label_encoder.inverse_transform(prediction)
