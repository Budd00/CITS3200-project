from django import forms
from .models import Tag
from django.forms.models import ModelMultipleChoiceField

class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class AssetForm(forms.Form):
    name = forms.CharField(max_length=100)
    public_notes = forms.CharField(widget=forms.Textarea)
    private_notes = forms.CharField(widget=forms.Textarea)

    #CHOICES = Tag.objects.all()

    tags = MyModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )


        #Tag.objects.values_list('name', flat=True)