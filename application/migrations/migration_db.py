import os
import sys
import snowflake.connector
from botocore.exceptions import ClientError
from pathlib import Path
from snowflake.connector.errors import DatabaseError, InterfaceError
from get_secrets import get_secrets_manager_values


def db_migrate():
    """connect to snowflake database and run database migration script"""
    try:
        secrets = get_secrets_manager_values()
    except ModuleNotFoundError as mnfe:
        raise mnfe
    except ImportError as ie:
        raise ie
    
    try:
        if None in secrets.values():
            raise ValueError(f'either its a wrong value in the creds or missing value/s')
        
    except ClientError as ce:
        raise ce
    except Exception as e:
        print(f'could not find file or something unexpected: {e}')
        raise e

    try:
        connection = snowflake.connector.connect(
                account  = secrets['ACCOUNT'],
                user     = secrets['USER'],
                password = secrets['PASSWORD'],
                role     = secrets['ROLE']
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
        sql_directory = Path(__file__).resolve().parent / 'sql'
        for sql_file in sorted(os.listdir(sql_directory)):
            if sql_file.endswith('.sql'):
                print(f'executing {sql_file}')
                with open(os.path.join(sql_directory, sql_file), 'r') as sql_script:
                    crud = sql_script.read() #read the entire SQL create script
                    cursor.execute(crud) #run the SQL script
          

    except FileNotFoundError as fnfe:
        print(f'error caught when trying to find SQL files: {fnfe}')
        raise fnfe

    except Exception as e:
        print(f'unexpected error: {e}')
        raise e

    finally:
        cursor.close()
        connection.close()
        print(f'closed snowflake connection')

if __name__ == '__main__':
    db_migrate() 

