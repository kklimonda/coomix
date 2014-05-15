from django import forms

from core.models import User

class UpdateSubscriptionsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('subscriptions',)
        widgets = {
            'subscriptions': forms.CheckboxSelectMultiple
        }
