from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# from django.template import loader
from django.urls import reverse
from .forms import UploadFileForm, ProcessFileForm, ProcessGroupFileForm
from .files import process_file_group, save_file, is_valid_file, process_single_file, is_valid_filter, file_exists

# Create your views here.


def index(request):
    upload_form = UploadFileForm()
    process_file_form = ProcessFileForm()
    process_group_form = ProcessGroupFileForm()
    return render(request=request, template_name="index.html", context={"upload_form": upload_form, "process_file_form": process_file_form, "process_group_form": process_group_form})


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if is_valid_file(request.FILES['file'].name):
                # Save file uploaded
                save_file(request.FILES['file'])
                print("File uploaded.")
            else:
                return HttpResponse("You must load a valid file.")

            return HttpResponseRedirect(redirect_to=reverse("data_loader:index"))


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
                    return HttpResponse("The file specified does not exist.")
            else:
                return HttpResponse("Invalid table selected.")
        else:
            return HttpResponse("An error has ocurred during form processing.")

        return HttpResponseRedirect(redirect_to=reverse("data_loader:index"))


def process_group(request):
    if request.method == "POST":
        form = ProcessGroupFileForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data.get('group')
            tablename = form.cleaned_data.get('table')
            if is_valid_filter(tablename=tablename, name=group, _type="group"):
                process_file_group(group, tablename)
            else:
                return HttpResponse("Invalid table selected.")
        else:
            return HttpResponse("An error has ocurred during form processing.")

        return HttpResponseRedirect(redirect_to=reverse("data_loader:index"))
