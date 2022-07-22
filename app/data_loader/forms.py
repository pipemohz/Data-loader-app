from django import forms
from .models import File, Table

files = [(file.name, file.name) for file in File.objects.all()]
tables = [(table.name, table.name) for table in Table.objects.all()]


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ProcessFileForm(forms.Form):
    file = forms.ChoiceField(required=True, choices=files)
    table = forms.ChoiceField(required=True, choices=tables)
