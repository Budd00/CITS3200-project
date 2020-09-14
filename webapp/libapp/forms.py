from django import forms
from .models import Tag, Asset
from django.forms.models import ModelMultipleChoiceField
from django.forms import ModelForm

class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class AssetItem(forms.Form):
    name = forms.CharField(
        max_length=100
    )
    public_notes = forms.CharField(widget=forms.Textarea, required = False)
    private_notes = forms.CharField(widget=forms.Textarea, required = False)
    tags = MyModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )

class AssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'pub_notes', 'priv_notes']


class TagForm(forms.Form):
    name = forms.CharField(max_length=100)
