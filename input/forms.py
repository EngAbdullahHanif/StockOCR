from django.forms import ModelForm
from django import forms
from django.forms.formsets import formset_factory

from .models import Item, macItem


class ItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['mac_img'].widget.attrs.update({'multiple'})
        mac_img = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta():
        model = Item
        fields = [
            'mac_img',
        ]

class MacForm(ModelForm):
    class Meta():
        model = macItem
        fields = [
            'mac',
            'img_path'
        ]

MacFormSet = formset_factory(MacForm, extra=0) 
