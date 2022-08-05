from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ProcessFileForm, ProcessGroupFileForm
from .files import process_file_group, process_single_file, is_valid_filter, file_exists
from django.contrib import messages

# Create your views here.


def index(request):
    process_file_form = ProcessFileForm()
    process_group_form = ProcessGroupFileForm()
    return render(request=request, template_name="index.html", context={"process_file_form": process_file_form, "process_group_form": process_group_form})


def process_file(request):
    if request.method == "POST":
        form = ProcessFileForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data.get('file')
            tablename = form.cleaned_data.get('table')
            if is_valid_filter(tablename=tablename, name=filename):
                if file_exists(filename=filename):
                    process_single_file(filename, tablename)
                else:
                    return HttpResponse("<h1>The file specified does not exist.</h1>")
            else:
                return HttpResponse("<h1>Invalid table selected.</h1>")
        else:
            return HttpResponse("<h1>1An error has ocurred during form processing.</h1>")

        messages.success(
            request, message=f"The file {filename} has been loaded to {tablename} database table.")
        return redirect('data_loader:index')


def process_group(request):
    if request.method == "POST":
        form = ProcessGroupFileForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data.get('group')
            tablename = form.cleaned_data.get('table')
            if is_valid_filter(tablename=tablename, name=group, _type="group"):
                process_file_group(group, tablename)
            else:
                return HttpResponse("<h1>Invalid table selected.</h1>")
        else:
            return HttpResponse("<h1>1An error has ocurred during form processing.</h1>")

        messages.success(
            request, message=f"The group of files {group} has been loaded to {tablename} database table.")
        return redirect('data_loader:index')
