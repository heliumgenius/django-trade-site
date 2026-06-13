from django import forms
from django.utils.translation import gettext_lazy as _


class CheckoutForm(forms.Form):
    name = forms.CharField(label=_("Contact Name"), max_length=100)
    company = forms.CharField(label=_("Company"), max_length=200, required=False)
    email = forms.EmailField(label=_("Email"))
    phone = forms.CharField(label=_("Phone"), max_length=50, required=False)
    address = forms.CharField(
        label=_("Address"), max_length=500,
        widget=forms.Textarea(attrs={"rows": 3})
    )
    city = forms.CharField(label=_("City"), max_length=100, required=False)
    country = forms.CharField(
        label=_("Country"), max_length=100, initial="China", required=False
    )


class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=100)
    company = forms.CharField(label=_("Company"), max_length=200, required=False)
    email = forms.EmailField(label=_("Email"))
    phone = forms.CharField(label=_("Phone"), max_length=50, required=False)
    product = forms.CharField(label=_("Product"), max_length=200, required=False)
    message = forms.CharField(
        label=_("Message"), max_length=2000,
        widget=forms.Textarea(attrs={"rows": 5})
    )
