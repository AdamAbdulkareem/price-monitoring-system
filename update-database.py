# Import necessary libraries
import MySQLdb
import json

# Function to create a table in the database for product history
def create_table():
    try:
        # Load product data from a JSON file
        with open("product_data.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
        
        # Connect to the MySQL database
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            port=3306,
            passwd="Adamabdul@paypal4040",
            db="price_monitor",
        )
        cursor = db.cursor()
        
        # Iterate through the product data and create a table for each product
        for key, item in data.items():
            product_id = item["ProductId"]
        
            # Insert into a product's price history table that already exists
            query_insert = "INSERT IGNORE INTO products (product_id) VALUES (%s)"
            cursor.execute(query_insert, (product_id,))
        
            # Create a table for the product's price history
            query = "CREATE TABLE IF NOT EXISTS `productshistory_{}`(`database_id`  int AUTO_INCREMENT NOT NULL , `product_name` varchar(255) NOT NULL ,`price` float NOT NULL ,`date_time` json NOT NULL ,`product_id` varchar(255) NOT NULL , PRIMARY KEY (`database_id`), FOREIGN KEY (`product_id`) REFERENCES `products`(`product_id`))".format(product_id)
            cursor.execute(query)
        
        # Commit changes and close the database connection
        db.commit()
        cursor.close()
        db.close()
        
    except FileNotFoundError as e:
        # Handle the case when the specified file is not found.
        print("Error: File not found.", e)
        
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors when reading the JSON file.
        print("Error: Unable to decode JSON from file.", e)
        
    except MySQLdb.Error as e:
        # Handle MySQL database errors that might occur during database operations.
        print("MySQL Error:", e)

# Function to update the product history table with new data
def update_table():
    try:
        # Load product data from a JSON file
        with open("product_data.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            
        # Connect to the MySQL database
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            port=3306,
            passwd="Adamabdul@paypal4040",
            db="price_monitor",
        )
        cursor = db.cursor()
        
        # Iterate through the product data and update the product history table
        for key, item in data.items():
            product_name = item["ProductName"]
            product_id = item["ProductId"]
            price = item["Price"]
            date_info = item["Date_Time"]

            # Insert new data into the product history table
            query = "INSERT INTO productshistory_{}(product_name, price, product_id, date_time) VALUES (%s, %s, %s, %s);".format(product_id)
            values = (product_name, price, product_id, json.dumps(date_info))
            cursor.execute(query,values)
            
        # Commit changes and close the database connection
        db.commit()
        cursor.close()
        db.close()
    
    except FileNotFoundError as e:
        # Handle the case when the specified file is not found.
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors when reading the JSON file.
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        # Handle MySQL database errors that might occur during database operations.
        print("MySQL Error:", e)
    
# Function to get the newest row of data for each product
def get_newest_row():
    newest_row_list = []
    try:
        # Load product data from a JSON file
        with open("product_data.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            
        # Connect to the MySQL database
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            port=3306,
            passwd="Adamabdul@paypal4040",
            db="price_monitor",
        )
        cursor = db.cursor()
        
        # Iterate through the product data and retrieve the newest row for each product
        for key, item in data.items():
            product_id = item["ProductId"]
            query = "SELECT product_name, price, product_id, date_time FROM ProductsHistory_{} ORDER BY database_id DESC LIMIT 1".format(product_id)
        
            cursor.execute(query)
            results = cursor.fetchone()
            newest_row_list.append(results)
        
        cursor.close()
        db.close()
        return (newest_row_list)
    
    except FileNotFoundError as e:
        # Handle the case when the specified file is not found.
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors when reading the JSON file.
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        # Handle MySQL database errors that might occur during database operations.
        print("MySQL Error:", e)

# Function to calculate and return the price change percentage for each product
def get_price_change():  # sourcery skip: for-append-to-extend, inline-variable
    price_change_arr = []
    percent_change_arr = []
    try:
        # Load product data from a JSON file
        with open("product_data.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
        
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            port=3306,
            passwd="Adamabdul@paypal4040",
            db="price_monitor",
        )
        
        #Iterate through the product data and calculate price changes
        for key, item in data.items():
            price_change_tuple = ()
            product_id = item["ProductId"]
    
            # Cursor for the entry price query
            cursor = db.cursor()
            entry_price_query = "SELECT price, database_id FROM productshistory_{} ORDER BY database_id ASC LIMIT 1".format(product_id)
            cursor.execute(entry_price_query)
            entry_price = cursor.fetchone()[0]
        
            price_change_tuple += (entry_price,)
            cursor.close()
    
            # Cursor for the current price query
            cursor = db.cursor()
            current_price_query = "SELECT price, database_id FROM productshistory_{} ORDER BY database_id DESC LIMIT 1".format(product_id)
            cursor.execute(current_price_query)
            current_price = cursor.fetchone()[0]
        
            price_change_tuple += (current_price,)
            cursor.close()
        
            price_change_arr.append(price_change_tuple)
    
        db.close()
    
        # Calculate percentage price changes and add to the result list
        for initial_price, final_price in price_change_arr:
            percent_change = (final_price - initial_price) / initial_price * 100
            percent_change_arr.append(round(percent_change, 2))
    
        return (percent_change_arr)
    
    
    except FileNotFoundError as e:
        # Handle the case when the specified file is not found.
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors when reading the JSON file.
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        # Handle MySQL database errors that might occur during database operations.
        print("MySQL Error:", e)
    
# Function to update the main products table in the database with new data
def update_db_table():
    try:
        with open("product_data.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            port=3306,
            passwd="Adamabdul@paypal4040",
            db="price_monitor",
        )
        cursor = db.cursor()
    
        newest_row = get_newest_row()
    
        # Update the main products table with new data
        for i in range(len(newest_row)):
            product_id = newest_row[i][2]
            product_name = newest_row[i][0]
            current_price = newest_row[i][1]
            price_change = get_price_change()[i]
            date_info = newest_row[i][3]
            query = "UPDATE products SET product_name = %s, current_price = %s, price_change = %s, date_time = %s WHERE product_id = %s"
            values = (product_name, current_price, price_change, json.dumps(date_info), product_id)
            cursor.execute(query,values)
        
        db.commit()
        cursor.close()
        db.close()
    
    except FileNotFoundError as e:
        # Handle the case when the specified file is not found.
        print("Error: File not found.", e)
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors when reading the JSON file.
        print("Error: Unable to decode JSON from file.", e)
    except MySQLdb.Error as e:
        # Handle MySQL database errors that might occur during database operations.
        print("MySQL Error:", e)
    
# Call the functions to perform the tasks
create_table() 
update_table()   
get_newest_row()
get_price_change()
update_db_table()
