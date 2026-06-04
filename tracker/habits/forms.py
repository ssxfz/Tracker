from django import forms
from .models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter habit title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter habit description',
                'rows': 4
            }),
        }

        labels = {
            'title': 'Habit title',
            'description': 'Description',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 3:
            raise forms.ValidationError('Habit title must be at least 3 characters long.')

        return title