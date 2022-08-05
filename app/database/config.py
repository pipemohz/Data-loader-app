import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get('host')
database = os.environ.get('database')
user = os.environ.get('user')
password = os.environ.get('password')
port = os.environ.get('port')


# Database connection string
conn_string = {
    'host': host,
    'database': database,
    'user': user,
    'password': password,
    'port': port
}
