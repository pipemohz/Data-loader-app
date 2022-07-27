from django import forms
from .models import File, FileGroup, Table


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ProcessFileForm(forms.Form):
    files = [(file.name, file.name)
             for file in File.objects.all() if not file.group]
    tables = [(table.name, table.name) for table in Table.objects.all()]
    file = forms.ChoiceField(required=True, choices=files)
    table = forms.ChoiceField(required=True, choices=tables)


class ProcessGroupFileForm(forms.Form):
    groups = [(group.name, group.name) for group in FileGroup.objects.all()]
    tables = [(table.name, table.name) for table in Table.objects.all()]
    group = forms.ChoiceField(required=True, choices=groups)
    table = forms.ChoiceField(required=True, choices=tables)
