# import psycopg2
# from sqlalchemy import create_engine, text
# import logging

# logging.basicConfig(level=logging.DEBUG)

# # Define the tool class using composition


# class CreatePostgresDatabaseAndSchemaTool:
#     def __init__(self, user: str, password: str, host: str, dbname: str):
#         self.user = user
#         self.password = password
#         self.host = host
#         self.dbname = dbname
#         self.default_dbname = "postgres"
#         self.default_engine = create_engine(
#             f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:5432/{self.default_dbname}")
#         self.new_db_engine = create_engine(
#             f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:5432/{self.dbname}")

#     def create_database(self):
#         # Connect to PostgreSQL default database to create a new one
#         conn = psycopg2.connect(
#             dbname="postgres",
#             user=self.user,
#             password=self.password,
#             host=self.host
#         )

#         # Set autocommit mode
#         conn.autocommit = True
#         cursor = conn.cursor()

#         try:
#             # SQL command to create a new database
#             cursor.execute(f"CREATE DATABASE {self.dbname};")
#             return f"Database '{self.dbname}' created successfully."
#         except psycopg2.Error as e:
#             return f"Error creating database: {e}"
#         finally:
#             cursor.close()
#             conn.close()

#     def create_tables(self):
#         # SQL commands to create tables
#         create_statements = [
#             """
#             CREATE TABLE IF NOT EXISTS GM_USER (
#                 user_id SERIAL PRIMARY KEY,
#                 username VARCHAR(50) NOT NULL,
#                 email VARCHAR(100) NOT NULL
#             );
#             """,
#             """
#             CREATE TABLE IF NOT EXISTS TENANT (
#                 tenant_id SERIAL PRIMARY KEY,
#                 tenant_name VARCHAR(100) NOT NULL
#             );
#             """,
#             """
#             CREATE TABLE IF NOT EXISTS TENANT_USER (
#                 tenant_user_id SERIAL PRIMARY KEY,
#                 tenant_id INT REFERENCES TENANT(tenant_id),
#                 user_id INT REFERENCES GM_USER(user_id)
#             );
#             """,
#             """
#             CREATE TABLE IF NOT EXISTS ROLE (
#                 role_id SERIAL PRIMARY KEY,
#                 role_name VARCHAR(50) NOT NULL
#             );
#             """,
#             """
#             CREATE TABLE IF NOT EXISTS PERMISSION (
#                 permission_id SERIAL PRIMARY KEY,
#                 permission_name VARCHAR(50) NOT NULL
#             );
#             """,
#             """
#             CREATE TABLE IF NOT EXISTS ROLE_PERMISSION (
#                 role_id INT REFERENCES ROLE(role_id),
#                 permission_id INT REFERENCES PERMISSION(permission_id),
#                 PRIMARY KEY(role_id, permission_id)
#             );
#             """,
#             """
#             CREATE TABLE IF NOT EXISTS USER_ROLE (
#                 user_id INT REFERENCES GM_USER(user_id),
#                 role_id INT REFERENCES ROLE(role_id),
#                 PRIMARY KEY(user_id, role_id)
#             );
#             """
#         ]

#         try:
#             with self.new_db_engine.connect() as connection:
#                 transaction = connection.begin()  # Start a transaction
#                 try:
#                     for statement in create_statements:
#                         logging.debug(f"Executing SQL: {statement}")
#                         result = connection.execute(text(statement))
#                         logging.debug(f"Result: {result}")
#                     transaction.commit()  # Commit the transaction
#                 except Exception as e:
#                     transaction.rollback()  # Rollback the transaction on error
#                     logging.error(f"Error during table creation: {e}")
#                     return f"Error creating tables: {e}"
#             return "Tables created successfully in the database."
#         except Exception as e:
#             return f"Error connecting to database or executing statements: {e}"

#     def run(self):
#         # Create the database and tables
#         db_creation_message = self.create_database()
#         table_creation_message = self.create_tables()
#         return f"{db_creation_message}\n{table_creation_message}"


# # Initialize and run the tool
# db_creation_tool = CreatePostgresDatabaseAndSchemaTool(
#     user="postgres",
#     password="1234",
#     host="localhost",
#     dbname="crewaii"
# )
# result = db_creation_tool.run()
# print(result)

import psycopg2
from sqlalchemy import create_engine, text
import logging

logging.basicConfig(level=logging.DEBUG)


def create_database(user: str, password: str, host: str, dbname: str) -> str:
    # Connect to PostgreSQL default database to create a new one
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host
    )

    # Set autocommit mode
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        # SQL command to create a new database
        cursor.execute(f"CREATE DATABASE {dbname};")
        return f"Database '{dbname}' created successfully."
    except psycopg2.Error as e:
        return f"Error creating database: {e}"
    finally:
        cursor.close()
        conn.close()


def create_tables(user: str, password: str, host: str, dbname: str) -> str:
    # Create engine for the new database
    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:5432/{dbname}")

    # SQL commands to create tables
    create_statements = [
        """
        CREATE TABLE IF NOT EXISTS GM_USER (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS TENANT (
            tenant_id SERIAL PRIMARY KEY,
            tenant_name VARCHAR(100) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS TENANT_USER (
            tenant_user_id SERIAL PRIMARY KEY,
            tenant_id INT REFERENCES TENANT(tenant_id),
            user_id INT REFERENCES GM_USER(user_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ROLE (
            role_id SERIAL PRIMARY KEY,
            role_name VARCHAR(50) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS PERMISSION (
            permission_id SERIAL PRIMARY KEY,
            permission_name VARCHAR(50) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS ROLE_PERMISSION (
            role_id INT REFERENCES ROLE(role_id),
            permission_id INT REFERENCES PERMISSION(permission_id),
            PRIMARY KEY(role_id, permission_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS USER_ROLE (
            user_id INT REFERENCES GM_USER(user_id),
            role_id INT REFERENCES ROLE(role_id),
            PRIMARY KEY(user_id, role_id)
        );
        """
    ]

    try:
        with engine.connect() as connection:
            transaction = connection.begin()  # Start a transaction
            try:
                for statement in create_statements:
                    logging.debug(f"Executing SQL: {statement}")
                    result = connection.execute(text(statement))
                    logging.debug(f"Result: {result}")
                transaction.commit()  # Commit the transaction
            except Exception as e:
                transaction.rollback()  # Rollback the transaction on error
                logging.error(f"Error during table creation: {e}")
                return f"Error creating tables: {e}"
        return "Tables created successfully in the database."
    except Exception as e:
        return f"Error connecting to database or executing statements: {e}"


def run(user: str, password: str, host: str, dbname: str) -> str:
    # Create the database and tables
    db_creation_message = create_database(user, password, host, dbname)
    table_creation_message = create_tables(user, password, host, dbname)
    return f"{db_creation_message}\n{table_creation_message}"


# Initialize and run the functions
result = run(
    user="postgres",
    password="1234",
    host="localhost",
    dbname="test"
)

print(result)
