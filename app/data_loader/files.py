from .models import *
import pandas as pd
import numpy as np
import os
from database.queries import queries_to_database


def is_valid_filter(tablename: str,  name: str, _type="file") -> bool:
    """
    Checks if there is at least one insertion rule for file or file group.

    ### Parameters 
    `tablename: str`
        Name of database table to insert data.
    `name: str` 
        Name of File or FileGroup object.
    `_type: str` 
        Optional. Type of object to check for insertions.
        If _type="file", the function will check for file insertions.
        If _type="group", the function will check for file group insertions.
        By default, _type="file".

    ### Returns
    `True` if file or file group has at least one insertion rule. `False` otherwise.
    """

    table = Table.objects.filter(name=tablename).first()

    if _type == "file":
        file = File.objects.filter(name=name).first()
        insertions = Insertion.objects.filter(file=file, table=table)
    elif _type == "group":
        group = FileGroup.objects.filter(name=name).first()
        insertions = GroupInsertion.objects.filter(group=group, table=table)

    if insertions:
        return True
    else:
        return False


def file_exists(filename: str):
    """
    Checks if file exists in files folder.
    ### Parameters 
    `filename: str`
        Name of the file.

    ### Returns
    `True` if file exists. `False` otherwise.
    """
    file = File.objects.filter(name=filename).first()

    if os.path.exists(file.filename.path):
        return True
    else:
        return False


def build_dataframe(path: str, columns: list) -> pd.DataFrame:
    """
    Builds a dataframe by reading file specified in path. Dataframe will only include columns specified by columns argument.

    ### Parameters 
    `path: str`
        File's path to read.
    `columns: list` 
        File's columns list to include in dataframe.

    ### Returns
    `pandas.Dataframe`
    """

    # Extract the name of the file from path
    filename = os.path.basename(path)

    if (filename.startswith("2") or filename.startswith("8")) and filename.endswith(".txt"):

        if '1-2' in columns:
            columns += columns[columns.index('1-2')].split('-')
            columns.remove('1-2')

        columns = [int(column)-1 for column in columns]

        header = (range(6))
        df = pd.read_csv(path, sep=';', header=0,
                         names=header, usecols=columns)
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)

        if 0 in columns and 1 in columns:
            df["name"] = df[0] + " " + df[1]
            df = df.drop(columns=[0, 1])
            columns.append("name")
            columns.remove(0)
            columns.remove(1)

        df = df.reindex(columns, axis="columns")

    elif "viabogo" in filename or "viacidis" in filename or "viaenv" in filename or "viafunza" in filename or "viayumbo" in filename or "viavegas" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df = df.reindex(columns, axis="columns")

    elif "carulla" in filename or "exitocol" in filename:
        df = pd.read_excel(path, engine='openpyxl', usecols=columns)
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.replace(
            to_replace=r'("id":)\w+[0-9,]|name:|[{}\[\]"]', value='', regex=True, inplace=True)
        if 'Roles' in columns:
            df = df.assign(Roles=df.Roles.str.split(',')).explode(
                'Roles', ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "SSFF" in filename:
        if "Primer nombre-Primer apellido" in columns:
            columns.insert(columns.index(
                "Primer nombre-Primer apellido"), "Primer nombre")
            columns.insert(columns.index(
                "Primer nombre-Primer apellido"), "Primer apellido")
            columns.remove("Primer nombre-Primer apellido")

        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)

        if "Primer nombre" in columns and "Primer apellido" in columns:
            df["name"] = df["Primer nombre"] + " " + df["Primer apellido"]
            df = df.drop(columns=["Primer nombre", "Primer apellido"])
            columns.insert(columns.index("Primer nombre"), "name")
            columns.remove("Primer nombre")
            columns.remove("Primer apellido")

        df = df.reindex(columns, axis="columns")

    elif "interactiva" in filename:

        columns = [int(column)-1 for column in columns]

        header = (range(9))
        df = pd.read_excel(path, engine='openpyxl', header=0,
                           names=header, usecols=columns, dtype='str')
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "POS" in filename:
        df = pd.read_excel(path, engine='xlrd', usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "HFM" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str', skiprows=3)
        df.ffill(inplace=True)
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "WMS_SCE" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "Teradata" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "MicroStrategy" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "ARIBA" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "Nplus" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "META4" in filename:
        df = pd.read_excel(path, engine='openpyxl',
                           usecols=columns, dtype='str')
        df.dropna(axis="index", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    elif "INFOPOS" in filename or "CIREC-WEB" in filename or "TFA" in filename:
        columns.append("HABILITADO")

        df = pd.read_csv(path, sep='\t', usecols=columns,
                         encoding='latin1', dtype='str')
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")
        df = df[df['HABILITADO'] == "SI"]
        df = df.drop(columns=['HABILITADO'])

    elif "SINCO" in filename or "SRCSPINFO" in filename:
        if "APL-CLA" in columns:
            columns.insert(columns.index("APL-CLA"), "APL")
            columns.insert(columns.index("APL-CLA"), "CLA")
            columns.remove("APL-CLA")

        df = pd.read_csv(path, sep=',', usecols=columns,
                         encoding='latin1', dtype='str')
        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)

        if "APL" in columns and "CLA" in columns:
            df["APL-CLA"] = df["APL"] + "-" + df["CLA"]
            df = df.drop(columns=["APL", "CLA"])
            columns.insert(columns.index("APL"), "APL-CLA")
            columns.remove("APL")
            columns.remove("CLA")

        df = df.reindex(columns, axis="columns")

    elif "SAP" in filename or "BW" in filename:
        df = pd.read_csv(path,
                         skiprows=3, sep=';', usecols=columns)
        if "SAP_USR02" in filename:
            df.replace(to_replace=r"\s{2,}",
                       value=np.nan, inplace=True, regex=True)

        df.dropna(axis='index', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.drop_duplicates(inplace=True, ignore_index=True)
        df = df.reindex(columns, axis="columns")

    return df


def process_single_file(filename: str, tablename: str):
    """
    Processes a file into a dataframe and makes queries to insert all dataframe records into database table.

    ### Parameters 
    `filename: str`
        Name of file to process.
    `table: str` 
        Name of database table to data insertion.
    """
    # Get File object by filename.
    file = File.objects.filter(name=filename).first()
    # Get Table object by filename.
    table = Table.objects.filter(name=tablename).first()

    # Get a list of Insertion objects by file and table.
    insertions = Insertion.objects.filter(file=file, table=table)

    # Build a strings list of column_from fields in Insertion objects list.
    columns_from = [i.column_from for i in insertions]
    # Build a strings list of column_to fields in Insertion objects list.
    columns_to = [i.column_to for i in insertions]

    # Check if there are special insertions for table.
    special_insertions = SpecialInsertion.objects.filter(
        file=file, table=table)

    # Build dataframe with file's data.
    df = build_dataframe(path=file.filename.path, columns=columns_from)

    # Make queries to insert all dataframe records into database table.
    queries_to_database(df=df, table=table.name,
                        columns_to=columns_to, system_id=file.system.id, special_insertions=special_insertions)


def process_file_group(groupname: str, tablename: str):
    """
    Processes a file group into a dataframe and makes queries to insert all dataframe records into database table.

    ### Parameters 
    `groupname: str`
        Name of file group to process.
    `table: str` 
        Name of database table to data insertion.
    """

    # Get FileGroup object by groupname.
    group = FileGroup.objects.filter(name=groupname).first()
    # Get Table object by filename.
    table = Table.objects.filter(name=tablename).first()

    # Get a list of File objects by group.
    files = File.objects.filter(group=group)

    # Get a list of GroupInsertion objects by group and table.
    insertions = GroupInsertion.objects.filter(group=group, table=table)

    # Build a strings list of column_from fields in GroupInsertion objects list.
    columns_from = [i.column_from for i in insertions]

    # Build a list of dataframes with data of each file in file group.
    dfs = [build_dataframe(path=file.filename.path,
                           columns=columns_from) for file in files]

    # Concatenate dataframes list into a single one
    df = pd.concat(dfs, ignore_index=True)
    # Delete duplicate records in dataframe.
    df.drop_duplicates(inplace=True)

    # Build a strings list of column_from fields in GroupInsertion objects list.
    columns_to = [i.column_to for i in insertions]

    # Make queries to insert all dataframe records into database table.
    queries_to_database(df=df, table=table.name,
                        columns_to=columns_to, system_id=files[0].system.id)
