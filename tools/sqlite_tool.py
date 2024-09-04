import sqlite3
from crewai_tools import tool


class SQLite3Tool:
    def __init__(self, database):
        self.database = database

    def connect(self):
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_table(self, create_table_sql):
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def insert_data(self, insert_sql, data):
        try:
            self.cursor.execute(insert_sql, data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)


@tool
def create_table(database, create_table_sql):
    """
    Creates a table in the SQLite database.

    Args:
    - database (str): Path to the SQLite database file.
    - create_table_sql (str): SQL query to create a table.

    Returns:
    - str: A message indicating the success of the table creation.

    Raises:
    - sqlite3.Error: If there's an error executing the SQL queries.
    """
    db_tool = SQLite3Tool(database)
    db_tool.connect()
    db_tool.create_table(create_table_sql)
    return "Table created successfully"


@tool
def insert_data(database, insert_sql, data):
    """
    Inserts data into a table in the SQLite database.

    Args:
    - database (str): Path to the SQLite database file.
    - insert_sql (str): SQL query to insert data into the table.
    - data (tuple): Data to insert into the table.

    Returns:
    - str: A message indicating the success of the data insertion.

    Raises:
    - sqlite3.Error: If there's an error executing the SQL queries.
    """
    db_tool = SQLite3Tool(database)
    db_tool.connect()
    db_tool.insert_data(insert_sql, data)
    return "Data inserted successfully"
