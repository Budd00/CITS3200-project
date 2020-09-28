from django import forms
from .models import Tag, Asset, AssetEdge
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