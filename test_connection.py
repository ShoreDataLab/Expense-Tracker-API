# test_connection.py
import pymysql
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_connection():
    try:
        # Connection parameters - use the exact ones that worked before
        params = {
            'host': 'localhost',  
            'user': 'root',
            'password': 'rootpassword',
            'database': 'EXPENSE_TRACKER',
            'port': 3306
        }
        
        logger.info(f"Attempting to connect with parameters: {params}")
        conn = pymysql.connect(**params)
        
        with conn.cursor() as cursor:
            cursor.execute('SELECT VERSION()')
            version = cursor.fetchone()
            logger.info(f"Successfully connected! Database version: {version}")
            
            # Test category table
            cursor.execute('SHOW CREATE TABLE Category')
            create_table = cursor.fetchone()
            logger.info(f"Category table structure: {create_table}")
            
        conn.close()
        logger.info("Connection closed successfully")
        
        # Print the exact connection string to use in SQLAlchemy
        sqlalchemy_url = f"mysql+pymysql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
        logger.info(f"SQLAlchemy connection string to use: {sqlalchemy_url}")
        
        return params
        
    except Exception as e:
        logger.error(f"Connection Error: {str(e)}")
        logger.error(f"Error Type: {type(e)}")
        raise

if __name__ == "__main__":
    working_params = test_connection()
    print("\nCopy these exact parameters to your config.py:")
    print("DB_CONFIG = {")
    for key, value in working_params.items():
        print(f"    '{key}': '{value}',")
    print("}")