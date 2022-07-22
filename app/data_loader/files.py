from django.core.files.uploadedfile import UploadedFile
from .models import *
import pandas as pd
import os
from app.settings import BASE_DIR
from data_loader.dao import query_database


def is_valid_filter(filename: str, tablename: str):

    file = File.objects.filter(name=filename).first()
    table = Table.objects.filter(name=tablename).first()

    sustitution = Sustitution.objects.filter(file=file, table=table)

    if sustitution:
        return True
    else:
        return False


def build_dataframe(path: str, columns: list) -> pd.DataFrame:

    filename = os.path.basename(path)

    if "csv" in filename or "txt" in filename:
        df = pd.read_csv(path,
                         skiprows=3, sep=';', usecols=columns)
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.columns = df.columns.str.replace(' ', '')

        # print(df.tail())

    return df


def process_file(filename: str, tablename: str):

    file = File.objects.filter(name=filename).first()
    table = Table.objects.filter(name=tablename).first()

    filename = file.filename
    system = file.system.name

    sustitutions = Sustitution.objects.filter(file=file, table=table)

    path_to_file = os.path.join(BASE_DIR, "files", system, filename)

    columns_from = [s.column_from for s in sustitutions]
    columns_to = [s.column_to for s in sustitutions]

    df = build_dataframe(path=path_to_file, columns=columns_from)
    query_database(df=df, table=table.name,
                   columns_to=columns_to, system_id=file.system.id)


def is_valid_file(filename: str) -> bool:
    files = File.objects.all()

    valid_file = any(file.filename == filename for file in files)

    if valid_file:
        return True
    else:
        return False


def save_file(file_object: UploadedFile):

    file = File.objects.filter(filename=file_object.name).first()

    # Set path to save file.
    path = os.path.join(BASE_DIR, "files")
    # Create "files" directory if not exist
    create_directory(path)
    # Set path of system to save file
    path = os.path.join(path, file.system.name)
    # Create system directory if not exist
    create_directory(path)

    with open(os.path.join(path, file_object.name), mode="wb+") as destination:
        for chunk in file_object.chunks():
            destination.write(chunk)


def create_directory(path: str):

    if not os.path.exists(path):
        os.mkdir(path)
