from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

class BloodDonationForm(forms.Form):
    bgroup_choices = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
        ("O+", "O+"), ("O-", "O-"),
    ]

    name = forms.CharField(
        label="Your Name",
        max_length = 50,
        widget = forms.TextInput(attrs={
            "placeholder": "e.g John Doe",
        }),
        required = True
    )
    age = forms.IntegerField(
        label = "Your Age",
        widget = forms.NumberInput(attrs={
            "placeholder": "e.g 25",
        }),
        help_text = "(18 - 70)",
        required = True
    )
    bgroup = forms.ChoiceField(
        label = "Your Blood Group",
        choices = bgroup_choices,
        required = True
    )
    height = forms.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(200)],
        help_text = "in cm",
        required = True
    )
    weight = forms.IntegerField(
        help_text = "in kg between (45 - 150)",
        required = True
    )
    med_history = forms.CharField(
        label = "Any Med History",
        widget = forms.Textarea(attrs={
            "style": "resize: none"
        })
    )
    recent_travel = forms.ChoiceField(
        label="Any Recent Travels?",
        widget = forms.RadioSelect,
        choices=[('Yes', 'Yes'), ('No', 'No')]
    )
    previous_donor = forms.ChoiceField(
        label="Have you previously Donated?",
        widget = forms.RadioSelect,
        choices=[('Yes', 'Yes'), ('No', 'No')]
    )
    latitude = forms.DecimalField(
        widget=forms.HiddenInput()
    )
    longitude = forms.DecimalField(
        widget=forms.HiddenInput()
    )

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 18 or age > 70:
            raise ValidationError("Your age must lie between the limits")
        return age
        
    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight < 45 or weight > 150:
            raise ValidationError("Your Weight must lie between the limits")
        return weight