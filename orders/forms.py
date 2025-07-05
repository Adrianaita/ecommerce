# orders/forms.py

from django import forms
from store.models import Order

class StatoOrdineForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['complete']
        labels = {'complete': 'Ordine completato'}
