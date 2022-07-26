from django.core.files.uploadedfile import UploadedFile
from .models import *
import pandas as pd
import numpy as np
import os
from app.settings import BASE_DIR
from data_loader.dao import query_database


def is_valid_filter(filename: str, tablename: str):

    file = File.objects.filter(name=filename).first()
    table = Table.objects.filter(name=tablename).first()

    insertions = Insertion.objects.filter(file=file, table=table)

    if insertions:
        return True
    else:
        return False


def file_exists(filename: str):
    file = File.objects.filter(name=filename).first()

    system = file.system.name

    if os.path.exists(os.path.join(BASE_DIR, "files", system, file.filename)):
        return True
    else:
        return False


def build_dataframe(path: str, columns: list) -> pd.DataFrame:

    filename = os.path.basename(path)

    if "report-roles-carulla-20102021" in filename:
        df = pd.read_excel(path, engine='openpyxl', usecols=columns)
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df["Roles"] = df["Roles"].str.split(':', expand=True)[1]
        df = df.reindex(columns, axis="columns")

    elif "INFOPOS" in filename or "CIREC-WEB" in filename or "TFA" in filename:
        columns.append("HABILITADO")

        df = pd.read_csv(path, sep='\t', usecols=columns, encoding='latin1')
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        # df.columns = df.columns.str.strip()
        df = df.reindex(columns, axis="columns")
        df = df[df['HABILITADO'] == "SI"]
        df = df.drop(columns=['HABILITADO'])

        if "DNI" in columns:
            df["DNI"] = df["DNI"].astype('str')

    elif "SINCO" in filename:
        df = pd.read_csv(path, sep=',', usecols=columns)
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        # df.columns = df.columns.str.strip()
        df = df.reindex(columns, axis="columns")

    elif "SAP" in filename or "BW" in filename:
        df = pd.read_csv(path,
                         skiprows=3, sep=';', usecols=columns)
        if filename == "SAP_USR02.csv":
            df.replace(to_replace=r"\s{2,}",
                       value=np.nan, inplace=True, regex=True)

        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        # df.columns = df.columns.str.strip()
        df = df.reindex(columns, axis="columns")

    df = df.head(5)
    print(df)

    return df


def process_file(filename: str, tablename: str):

    file = File.objects.filter(name=filename).first()
    table = Table.objects.filter(name=tablename).first()

    filename = file.filename
    system = file.system.name

    insertions = Insertion.objects.filter(file=file, table=table)

    path_to_file = os.path.join(BASE_DIR, "files", system, filename)

    columns_from = [i.column_from for i in insertions]
    columns_to = [i.column_to for i in insertions]

    # Check if there are special insertions for table.
    special_insertions = SpecialInsertion.objects.filter(
        file=file, table=table)

    df = build_dataframe(path=path_to_file, columns=columns_from)
    query_database(df=df, table=table.name,
                   columns_to=columns_to, system_id=file.system.id, special_insertions=special_insertions)


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
