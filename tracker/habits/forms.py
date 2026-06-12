from django import forms
from .models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'use_timer', 'required_minutes']

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
            'use_timer': forms.CheckboxInput(attrs={
                "class": "form-check-input",
                'id': 'id_use_timer',
            }),
            'required_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 240,
                'id': 'id_required_minutes',
            })
        }

        labels = {
            'title': 'Habit title',
            'description': 'Description',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        use_timer = self.cleaned_data.get('use_timer')
        required_minutes = self.cleaned_data.get('required_minutes')
        cleaned_data = super(HabitForm, self).clean()

        if use_timer and not required_minutes:
            self.add_error('use_timer', f'Required minutes required for {title}')

        if len(title) < 3:
            raise forms.ValidationError('Habit title must be at least 3 characters long.')

        return title
