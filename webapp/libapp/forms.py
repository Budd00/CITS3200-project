from django import forms

class AssetForm(forms.Form):
    name = forms.CharField(max_length=100)
    public_notes = forms.CharField(widget=forms.Textarea)
    private_notes = forms.CharField(widget=forms.Textarea)