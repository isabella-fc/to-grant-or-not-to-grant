from django import forms
from dal import autocomplete
from wcb.models import NYZipCode


class ModelForm(forms.Form):
    # Numeric fields
    accident_date = forms.DateField(label='Accident Date', widget=forms.DateInput(attrs={'type': 'date'}))
    age_at_injury = forms.IntegerField(label='Age at Injury')
    assembly_date = forms.DateField(label='Assembly Date', widget=forms.DateInput(attrs={'type': 'date'}))
    average_weekly_wage = forms.DecimalField(label='Average Weekly Wage', decimal_places=2, max_digits=10)
    birth_year = forms.IntegerField(label='Birth Year')
    ime4_count = forms.IntegerField(label='IME-4 Count')
    number_of_dependents = forms.IntegerField(label='Number of Dependents')

    # Boolean fields
    attorney_representative = forms.ChoiceField(
        label='Attorney/Representative',
        choices=[(True, 'True'), (False, 'False')],
        widget=forms.RadioSelect
    )
    covid_indicator = forms.ChoiceField(
        label='COVID-19 Indicator',
        choices=[(True, 'True'), (False, 'False')],
        widget=forms.RadioSelect
    )

    # Select fields (categorical)
    carrier_type = forms.ChoiceField(
        label='Carrier Type',
        choices=[
            ('1A. PRIVATE', '1A. PRIVATE'),
            ('2A. SIF', '2A. SIF'),
            ('3A. SELF PUBLIC', '3A. SELF PUBLIC'),
            ('Other', 'Other')
        ]
    )

    gender = forms.ChoiceField(
        label='Gender',
        choices=[('F', 'Female'), ('M', 'Male')]
    )

    # Text input fields
    district_name = forms.CharField(label='District Name', max_length=50)
    medical_fee_region = forms.CharField(label='Medical Fee Region', max_length=50)
    carrier_name = forms.CharField(label='Carrier Name', max_length=50)
    county_of_injury = forms.CharField(label='County of Injury', max_length=50)
    industry_code = forms.CharField(label='Industry Code', max_length=10)
    wcio_cause_of_injury_code = forms.CharField(label='WCIO Cause of Injury Code', max_length=10)
    wcio_nature_of_injury_code = forms.CharField(label='WCIO Nature of Injury Code', max_length=10)
    wcio_part_of_body_code = forms.CharField(label='WCIO Part of Body Code', max_length=10)

    zip_code = forms.CharField(
        label='Zip Code',
        widget=forms.TextInput(attrs={'list': 'zip_codes', 'class': 'form-control'})
    )






