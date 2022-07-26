from django import forms
from .models import File, Table


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ProcessFileForm(forms.Form):
    files = [(file.name, file.name) for file in File.objects.all()]
    tables = [(table.name, table.name) for table in Table.objects.all()]
    file = forms.ChoiceField(required=True, choices=files)
    table = forms.ChoiceField(required=True, choices=tables)
