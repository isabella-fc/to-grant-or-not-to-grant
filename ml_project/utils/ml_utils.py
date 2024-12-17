import os
import pandas as pd
import numpy as np
import pickle
from django.conf import settings
from sklearn.preprocessing import RobustScaler
import re


def preprocess_form(form_data):
    """
    Preprocesses the input DataFrame from the form by applying all transformations
    in the correct feature order, handling missing columns gracefully.
    """
    # Define the correct feature order
    feature_order = [
        'Accident Date',
        'Age at Injury',
        'Assembly Date',
        'Average Weekly Wage',
        'Birth Year',
        'IME-4 Count',
        'Number of Dependents',
        'Attorney/Representative_False',
        'Attorney/Representative_True',
        'Carrier Type_1A. PRIVATE',
        'Carrier Type_2A. SIF',
        'Carrier Type_3A. SELF PUBLIC',
        'COVID-19 Indicator_False',
        'COVID-19 Indicator_True',
        'District Name_NYC',
        'Gender_F',
        'Gender_M',
        'Medical Fee Region_IV',
        'Carrier Name',
        'County of Injury',
        'Industry Code',
        'WCIO Cause of Injury Code',
        'WCIO Nature of Injury Code',
        'WCIO Part Of Body Code',
        'Zip Code'
    ]

    # Ensure all expected columns exist in the input DataFrame
    for col in feature_order:
        if col not in form_data.columns:
            # Initialize missing columns with default values
            if col in ['Attorney/Representative_False', 'Attorney/Representative_True',
                       'Carrier Type_1A. PRIVATE', 'Carrier Type_2A. SIF',
                       'Carrier Type_3A. SELF PUBLIC', 'COVID-19 Indicator_False',
                       'COVID-19 Indicator_True', 'District Name_NYC',
                       'Gender_F', 'Gender_M', 'Medical Fee Region_IV']:
                form_data[col] = 0  # Default for boolean columns
            else:
                form_data[col] = np.nan  # Default for other columns

    # Process numerical columns for scaling
    scale_form = [
        'Accident Date', 'Assembly Date', 'Average Weekly Wage',
        'Age at Injury', 'Birth Year', 'Number of Dependents', 'IME-4 Count'
    ]
    scaler = RobustScaler()
    for col in scale_form:
        if col in form_data.columns:
            form_data[col] = pd.to_numeric(form_data[col], errors='coerce')
            form_data[col] = scaler.fit_transform(form_data[[col]])

    # Process categorical columns for frequency encoding
    encoding_frequency1_form = [
        'Carrier Name', 'Industry Code', 'WCIO Cause of Injury Code',
        'WCIO Nature of Injury Code', 'WCIO Part Of Body Code',
        'Zip Code', 'County of Injury'
    ]
    for col in encoding_frequency1_form:
        if col in form_data.columns:
            freq_dict = form_data.groupby(col).size() / len(form_data)
            form_data[col] = form_data[col].map(freq_dict).fillna(0)

    # Process date columns to timestamps
    date_form = ['Accident Date', 'Assembly Date']
    for col in date_form:
        if col in form_data.columns:
            form_data[col] = pd.to_datetime(form_data[col], errors='coerce')
            form_data[col] = form_data[col].apply(lambda x: x.timestamp() if pd.notnull(x) else np.nan)

    # Ensure final DataFrame columns are in the correct order
    form_data = form_data[feature_order]

    return form_data


def decode_prediction(prediction):
    """
    Decodes the model prediction into a readable format.
    """

    # open label encoder
    with (open(os.path.join(settings.BASE_DIR, 'ml_project', 'ml_model', 'label_encoder.pkl'), 'rb')
          as le_file): label_encoder = pickle.load(le_file)

    return label_encoder.inverse_transform(prediction)
