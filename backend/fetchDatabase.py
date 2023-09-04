import MySQLdb
from os import environ as env
from dotenv import load_dotenv

# Call the function to load variables from .env file into the environment
load_dotenv()

def get_mysql_connection():
    try:
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            port=3306,
            passwd=env["DB_PASSWORD"],
            db="price_monitor",
        )
        return db
        
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
def fetch_dbProduct(product_ASIN):
    db = get_mysql_connection()
    cursor = db.cursor()
    
    # Define the SQL query to fetch records by product ASIN
    query = "SELECT * FROM productshistory_{} WHERE product_id = %s".format(product_ASIN)
    
    # Execute the SQL query with the provided product ASIN
    cursor.execute(query, (product_ASIN,))
    
    results = cursor.fetchall()
    cursor.close()
    db.close()
    
    return results