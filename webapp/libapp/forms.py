from django import forms
from .models import Tag, Asset, AssetEdge, AlternateName
from django.forms.models import ModelMultipleChoiceField, ModelChoiceField, ModelChoiceIterator
from django.forms import ModelForm, MultipleChoiceField, ChoiceField

class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)

    choices = property(_get_choices, MultipleChoiceField._set_choices)


class CustomModelChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj), self.field.label_from_instance(obj), obj)

class AssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'pub_notes', 'priv_notes', 'tags']

    tags = MyModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )

class TagForm(forms.Form):
    name = forms.CharField(max_length=100)
    alt_names = forms.CharField(required = False, max_length=200, label = "Provide any alternate names for this tag. Seperate each name with a comma and a space.")


    parent_tags = MyModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )

    child_tags = MyModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )

class TagEditForm(forms.Form):
    name = forms.CharField(max_length=100)
    new_alts = forms.CharField(required = False, max_length=200, label = "Provide any alternate names for this tag. Seperate each name with a comma and a space.")
