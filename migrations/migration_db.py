import os
import snowflake.connector
from snowflake.connector.errors import DatabaseError, InterfaceError
from dotenv import load_dotenv

def db_migrate():
    """connect to snowflake database and run database migration script"""

    try:
        load_dotenv()
        sf_cred = {
            'account': os.environ.get('ACCOUNT'),
            'user': os.environ.get('USER'),
            'password': os.environ.get('PASSWORD'),
            'role': os.environ.get('ROLE')
        }
        if None in sf_cred.values():
            raise ValueError(f'either its a wrong value in the creds or missing value/s')
    
    except Exception as e:
        print(f'could not find file or something unexpected: {e}')
        raise e

    try:
        connection = snowflake.connector.connect(
                account = sf_cred['account'],
                user = sf_cred['user'],
                password = sf_cred['password'],
                role = sf_cred['role']
            )
        cursor = connection.cursor()
        print(f'successful connection to snowflake')

    except InterfaceError as ie:
        print(f'network or parameter issue: {ie}')
        raise ie

    except DatabaseError as de:
        print(f'authentication or database error: {de}')
        raise de

    except Exception as e:
        print(f'unexpected error: {e}')
        raise e


    
    try:
        sql_directory = 'sql'
        for sql_file in sorted(os.listdir(sql_directory)):
            if sql_file.endswith('.sql'):
                print(f'executing {sql_file}')
                with open(os.path.join(sql_directory, sql_file), 'r') as sql_script:
                    crud = sql_script.read() #read the entire SQL create script
                    cursor.execute(crud) #run the SQL script
          

    except FileNotFoundError as fnfe:
        print(f'error caught when trying to find SQL files: {e}')
        raise e

    except Exception as e:
        print(f'unexpected error: {e}')
        raise e

    finally:
        cursor.close()
        connection.close()
        print(f'closed snowflake connection')

if __name__ == '__main__':
    db_migrate() 

