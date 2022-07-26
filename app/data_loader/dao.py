import psycopg2
from pandas import DataFrame


def query_database(df: DataFrame, table: str, columns_to: list, system_id: int, special_insertions=None):
    """
    Make a query to DB_NAME database of SQL Server DB_HOST.
    """
    # Database connection

    conn_string = {
        "host": "localhost",
        "database": "maximize",
        "user": "Pipe",
        "password": "1234",
        "port": "49153"
    }
    # Initialize connection object to postgres database
    conn = psycopg2.connect(**conn_string)

    # Initialize cursor to execute commands on database
    cursor = conn.cursor()

    if special_insertions:
        for si in special_insertions:
            columns_to.append(si.column_to)

        values = [si.value for si in special_insertions]

        columns_to.append('system_id')

        # Execution of query in Database.
        for _, row in df.iterrows():
            r = row.str.replace("'", "´")
            r = r.str.strip().to_list()
            r += values
            r.append(system_id)
            query = f"INSERT INTO {table} ({', '.join(columns_to)}) VALUES {tuple(r)}"
            print(query)
        #     cursor.execute(query)

    else:
        columns_to.append('system_id')
        # Execution of query in Database.
        for _, row in df.iterrows():
            r = row.str.replace("'", "´")
            r = r.str.strip().to_list()
            r.append(system_id)
            query = f"INSERT INTO {table} ({', '.join(columns_to)}) VALUES {tuple(r)}"
            print(query)
        #     cursor.execute(query)

    # conn.commit()

    cursor.close()
    conn.close()

    print("Execution finished.")
