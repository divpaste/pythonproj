from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    bgroup = forms.ChoiceField(
        choices=User.bgroup_choices,
        required=True,
        label="Blood Group"
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "bgroup"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.bgroup = self.cleaned_data["bgroup"]
        if commit:
            user.save()
        return user

class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = User 

        fields = (
        "full_name","age","bgroup","height","weight","med_history","previous_donor","contact","longitude","latitude"
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "e.g John Doe",}),
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