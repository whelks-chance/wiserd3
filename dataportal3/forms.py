__author__ = 'ubuntu'

from django import forms
from models import ShapeFileUpload


class ShapefileForm(forms.ModelForm):
    """
    to handle uploading grades csv file
    """
    class Meta:
        fields = ['shapefile']
        model = ShapeFileUpload