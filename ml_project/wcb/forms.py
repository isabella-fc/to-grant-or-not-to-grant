from django import forms

class ModelForm(forms.Form):
    # Numeric fields
    accident_date = forms.DateField(label='Accident Date', widget=forms.DateInput(attrs={'type': 'date'}))
    c2_date = forms.DateField(label='Date of Receipt C-2 Form or Equivalent',
                              widget=forms.DateInput(attrs={'type': 'date'}))
    age_at_injury = forms.IntegerField(label='Age at Injury')
    assembly_date = forms.DateField(label='Assembly Date', widget=forms.DateInput(attrs={'type': 'date'}))
    average_weekly_wage = forms.DecimalField(label='Average Weekly Wage', decimal_places=2, max_digits=10)
    birth_year = forms.IntegerField(label='Birth Year')
    ime4_count = forms.IntegerField(label='IME-4 Count')
    number_of_dependents = forms.IntegerField(label='Number of Dependents')

    # Boolean fields
    attorney_representative = forms.ChoiceField(
        label='Attorney/Representative',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect
    )
    covid_indicator = forms.ChoiceField(
        label='COVID-19 Indicator',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect
    )
    c3_form_submitted = forms.ChoiceField(
        label='Was a C-3 Form Submitted?',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect
    )
    first_hearing_date = forms.ChoiceField(
        label='Was a First Hearing Held?',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect
    )
    alternative_dispute_resolution = forms.ChoiceField(
        label='Was Alternative Dispute Resolution Used?',
        choices=[(True, 'Yes'), (False, 'No'), (None, 'Unknown')],
        widget=forms.RadioSelect
    )

    # Select fields (categorical)
    carrier_type = forms.ChoiceField(
        label='Carrier Type',
        choices=[
            ('1A. PRIVATE', '1A. PRIVATE'),
            ('2A. SIF', '2A. SIF'),
            ('3A. SELF PUBLIC', '3A. SELF PUBLIC'),
            ('4A. SELF PRIVATE', '4A. SELF PRIVATE'),
            ('5A. SPECIAL FUND - CONS. COMM. (SECT. 25-A)', '5A. SPECIAL FUND - CONS. COMM. (SECT. 25-A)'),
            ('5C. SPECIAL FUND - POI CARRIER WCB MENANDS', '5C. SPECIAL FUND - POI CARRIER WCB MENANDS'),
            ('5D. SPECIAL FUND - UNKNOWN', '5D. SPECIAL FUND - UNKNOWN'),
            ('Other', 'Other')
        ]
    )

    gender = forms.ChoiceField(
        label='Gender',
        choices=[('F', 'Female'),
                 ('M', 'Male'),
                 ('U', 'Did not report'),
                 ('X', 'Other'),
                 ]
    )

    # Text input fields
    district_name = forms.ChoiceField(
        label='District Name',
        choices=[
            ('ALBANY', 'Albany'),
            ('BINGHAMTON', 'Binghamton'),
            ('BUFFALO', 'Buffalo'),
            ('HAUPPAUGE', 'Hauppauge'),
            ('NYC', 'NYC'),
            ('ROCHESTER', 'Rochester'),
            ('STATEWIDE', 'Statewide'),
            ('SYRACUSE', 'Syracuse'),
            (None, 'Other'),
        ]
    )
    medical_fee_region = forms.ChoiceField(
        label='Medical Fee Region',
        choices=[
            ('Medical Fee Region_I', 'Region I'),
            ('Medical Fee Region_II', 'Region II'),
            ('Medical Fee Region_III', 'Region III'),
            ('Medical Fee Region_IV', 'Region IV'),
            ('Medical Fee Region_UK', 'Other'),
        ]
    )

    county_of_injury = forms.ChoiceField(
        label='County of Injury',
        choices=[
            ('ALBANY', 'Albany'),
            ('ALLEGANY', 'Allegany'),
            ('BRONX', 'Bronx'),
            ('BROOME', 'Broome'),
            ('CATTARAUGUS', 'Cattaraugus'),
            ('CAYUGA', 'Cayuga'),
            ('CHAUTAUQUA', 'Chautauqua'),
            ('CHEMUNG', 'Chemung'),
            ('CHENANGO', 'Chenango'),
            ('CLINTON', 'Clinton'),
            ('COLUMBIA', 'Columbia'),
            ('CORTLAND', 'Cortland'),
            ('DELAWARE', 'Delaware'),
            ('DUTCHESS', 'Dutchess'),
            ('ERIE', 'Erie'),
            ('ESSEX', 'Essex'),
            ('FRANKLIN', 'Franklin'),
            ('FULTON', 'Fulton'),
            ('GENESEE', 'Genesee'),
            ('GREENE', 'Greene'),
            ('HAMILTON', 'Hamilton'),
            ('HERKIMER', 'Herkimer'),
            ('JEFFERSON', 'Jefferson'),
            ('KINGS', 'Kings'),
            ('LEWIS', 'Lewis'),
            ('LIVINGSTON', 'Livingston'),
            ('MADISON', 'Madison'),
            ('MONROE', 'Monroe'),
            ('MONTGOMERY', 'Montgomery'),
            ('NASSAU', 'Nassau'),
            ('NEW YORK', 'New York'),
            ('NIAGARA', 'Niagara'),
            ('ONEIDA', 'Oneida'),
            ('ONONDAGA', 'Onondaga'),
            ('ONTARIO', 'Ontario'),
            ('ORANGE', 'Orange'),
            ('ORLEANS', 'Orleans'),
            ('OSWEGO', 'Oswego'),
            ('OTSEGO', 'Otsego'),
            ('PUTNAM', 'Putnam'),
            ('QUEENS', 'Queens'),
            ('RENSSELAER', 'Rensselaer'),
            ('RICHMOND', 'Richmond'),
            ('ROCKLAND', 'Rockland'),
            ('SARATOGA', 'Saratoga'),
            ('SCHENECTADY', 'Schenectady'),
            ('SCHOHARIE', 'Schoharie'),
            ('SCHUYLER', 'Schuyler'),
            ('SENECA', 'Seneca'),
            ('ST. LAWRENCE', 'St. Lawrence'),
            ('STEUBEN', 'Steuben'),
            ('SUFFOLK', 'Suffolk'),
            ('SULLIVAN', 'Sullivan'),
            ('TIOGA', 'Tioga'),
            ('TOMPKINS', 'Tompkins'),
            ('ULSTER', 'Ulster'),
            ('UNKNOWN', 'Unknown'),
            ('WARREN', 'Warren'),
            ('WASHINGTON', 'Washington'),
            ('WAYNE', 'Wayne'),
            ('WESTCHESTER', 'Westchester'),
            ('WYOMING', 'Wyoming'),
            ('YATES', 'Yates'),
        ]
    )
    industry_code = forms.CharField(label='Industry Code', max_length=10, required=False)
    wcio_cause_of_injury_code = forms.CharField(label='WCIO Cause of Injury Code', max_length=10, required=False)
    wcio_nature_of_injury_code = forms.CharField(label='WCIO Nature of Injury Code', max_length=10, required=False)
    wcio_part_of_body_code = forms.CharField(label='WCIO Part of Body Code', max_length=10, required=False)

    zip_code = forms.CharField(
        label='Zip Code',
        widget=forms.TextInput(attrs={
            'list': 'zip_codes',
            'class': 'form-control',
            'placeholder': 'Search zip codes...'
        })
    )

    carrier_name = forms.CharField(
        label='Carrier Name',
        widget=forms.TextInput(attrs={
            'list': 'carrier_names',
            'class': 'form-control',
            'placeholder': 'Search carrier name...'
        })
    )
