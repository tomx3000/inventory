from django import forms
from .models import Sales,Store,Employee,Company,Customer,Inventory,Item


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields='__all__'