from curses.ascii import controlnames
import psycopg2
import csv
import os

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS accounts (
            customer_id INT PRIMARY KEY NOT NULL, 
            first_name VARCHAR(255) NOT NULL, 
            last_name VARCHAR(255) NOT NULL, 
            address_1 VARCHAR(255), 
            address_2 VARCHAR(255), 
            city VARCHAR(255), 
            state VARCHAR(255), 
            zip_code VARCHAR(10), 
            join_date DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY NOT NULL, 
            product_code SMALLINT NOT NULL, 
            product_description VARCHAR(255)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id VARCHAR(30) PRIMARY KEY, 
            transaction_date DATE, 
            product_id INT,
            FOREIGN KEY(product_id)
                REFERENCES products(product_id)
                ON UPDATE CASCADE ON DELETE CASCADE, 
            product_code SMALLINT, 
            product_description VARCHAR(255), 
            quantity INT, 
            account_id INT,
            FOREIGN KEY(account_id)
                REFERENCES accounts(customer_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    ]
    return commands

def delete_tables():
    commands = [
        '''
        DROP TABLE IF EXISTS accounts
        ''',
        '''
        DROP TABLE IF EXISTS products
        ''',
        '''
        DROP TABLE IF EXISTS transactions
        '''
    ]
    return commands

def main():
    host = 'postgres'
    database = 'postgres'
    user = 'postgres'
    pas = 'postgres'
    port = 5432
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas, port=port)
    cur = conn.cursor()
    commands = create_tables()
    
    cur.execute(commands[0])
    cur.execute(commands[1])
    cur.execute(commands[2])

    
    file_path = './data/'
    # Read each csv file in data directory
    for root, dirs, files in os.walk(file_path):
        for file in files:
            tbl = file.split('.')
            print(file_path+file)
            with open(file_path + file, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if tbl[0] == 'accounts':
                        cur.execute(
                            "INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?,?)", (row[0], row[1],row[2], row[3],row[4], row[5],row[6], row[7],row[8]))
                    elif tbl[0] == 'products':
                        cur.execute(
                            "INSERT INTO products VALUES (?,?,?)", (row[0], row[1],row[2]))
                    else:
                        cur.execute(
                            "INSERT INTO transactions VALUES (?,?,?,?,?,?,?)", (row[0], row[1],row[2], row[3],row[4], row[5],row[6]))
                    conn.commit()

    print(cur.execute("select * from products"))
    cur.close()


if __name__ == '__main__':
    main()
