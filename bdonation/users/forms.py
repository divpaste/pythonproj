from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Donor
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ["username", "password1", "password2"]

class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = Donor 

        fields = (
        "name","age","bgroup","height","weight","med_history","previous_donor","contact","longitude","latitude"
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g John Doe",}),
            "age": forms.NumberInput(attrs={"placeholder": "e.g 25",}),
            "bgroup": forms.Select(),
            "height": forms.NumberInput(attrs={"placeholder": "cm"}),
            "weight": forms.NumberInput(attrs={"placeholder": "kg"}),
            "med_history": forms.Textarea(attrs={"style": "resize: none"}),
            "contact": forms.TextInput(attrs={"placeholder": "+91 98502 xxxxx"}),
            "previous_donor": forms.RadioSelect(choices=[(True, "Yes"), (False, "No")]),
            "longitude": forms.HiddenInput(),  
            "latitude": forms.HiddenInput()
        }
        help_texts = {
            "age": "18 to 70",
            "contact" : "10 digits",
            "height": "in cms",
            "weight": "in kgs",
        }

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