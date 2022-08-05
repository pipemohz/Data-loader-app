import psycopg2
from pandas import DataFrame, Series
from .config import conn_string


def queries_to_database(df: DataFrame, table: str, columns_to: list, system_id: int, special_insertions=None):
    """
    Makes a series of queries to postgresql database with data from Dataframe object.
    ### Parameters 
    `df: pandas.Dataframe`
        Dataframe with file data.
    `table: str` 
        Name of database table to insert data.
    `columns_to: list` 
        Names list of database table columns to data insertion.
    `system_id: int` 
        Id of the external system of origin of data.
    `special_insertions: list|None` 
        Optional argument. If it is specified must be a list of SpecialInsertion objects.
    """

    # Initialize connection object to postgres database
    conn = psycopg2.connect(**conn_string)

    # Declare a cursor inside conn context manager
    with conn:
        with conn.cursor() as cursor:

            if special_insertions:
                for si in special_insertions:
                    columns_to.append(si.column_to)

                values = [si.value for si in special_insertions]

                columns_to.append('system_id')
                # Execution of query in Database.
                for _, row in df.iterrows():
                    make_query(cursor, row, system_id, table,
                               columns_to, values=values)

            else:
                columns_to.append('system_id')
                # Execution of query in Database.
                for _, row in df.iterrows():
                    make_query(cursor, row, system_id, table, columns_to)

            conn.commit()

    conn.close()


def make_query(cursor, row: Series, system_id: int, table: str, columns_to: list, values=None):
    """
    Makes a query to postgresql database.
    ### Parameters 
    `cursor: psycopg2.cursor`
        Psycopg2 connection cursor object.
    `row: pandas.Series` 
        Series with data of one row record from dataframe.
    `system_id: int` 
        Id of the external system of origin of data.
    `columns_to: list` 
        Names list of database table columns to data insertion.
    `values: list|None` 
        Optional argument. If it is specified must be a list of values related to SpecialInsertion rules for file.
    """
    r = row.str.replace("'", "´")
    r = r.str.strip().to_list()
    if values:
        r += values
    r.append(system_id)

    query = f"INSERT INTO {table} ({', '.join(columns_to)}) VALUES {tuple(r)}"

    cursor.execute(query)
