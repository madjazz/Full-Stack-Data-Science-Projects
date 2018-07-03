from django import forms
from .models import Log


class MoodForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MoodForm, self).__init__(*args, **kwargs)
        self.fields['mood_field'].label = False

    class Meta:
        model = Log
        fields = ('mood_field', )
        widgets = {
            'name': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
