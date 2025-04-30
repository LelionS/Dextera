from django import forms
from .models import WeekEntry

class WeekEntryForm(forms.ModelForm):
    class Meta:
        model = WeekEntry
        fields = ['week', 'bay', 'bed', 'variety', 'amounts']  # Ensure field names match the model
