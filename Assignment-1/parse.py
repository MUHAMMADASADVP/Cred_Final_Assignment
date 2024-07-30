import pandas as pd
import psycopg2
from psycopg2 import sql

df = pd.read_csv('customers.csv')

def format_data(row):
    row['f_name'] = row['First Name'].upper()
    row['l_name'] = row['Last Name'].upper()
    row['personal_email'] = row['Email'].lower()
    row['full_name'] = f"{row['First Name']} {row['Last Name']}"
    row['work_email'] = f"{row['First Name'].lower()}_{row['Last Name'].lower()}@sample.com"
    return row

df = df.apply(format_data, axis=1)

conn = psycopg2.connect(
    host="localhost",
    database="Newdb",
    user="postgres",
    password="root"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_info (
        customer_id CHAR(15) PRIMARY KEY,
        f_name VARCHAR(50) NOT NULL,
        l_name VARCHAR(50) NOT NULL,
        city VARCHAR(50),
        country VARCHAR(50),
        personal_phnum VARCHAR(50),
        personal_email VARCHAR(100) UNIQUE
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS customer_work_info (
        customer_id CHAR(15) PRIMARY KEY,
        full_name VARCHAR(101) NOT NULL,
        office_loc VARCHAR(50) DEFAULT 'Bangalore',
        subscription_date DATE,
        website VARCHAR(100),
        work_phnum VARCHAR(50),
        work_email VARCHAR(100) UNIQUE
    );
""")

for _, row in df.iterrows():
    cur.execute(
        sql.SQL("INSERT INTO customer_info (customer_id, f_name, l_name, city, country, personal_phnum, personal_email) VALUES (%s, %s, %s, %s, %s, %s, %s)"),
        [row['Customer Id'], row['f_name'], row['l_name'], row['City'], row['Country'], row['Phone 1'], row['personal_email']]
    )
    
    cur.execute(
        sql.SQL("INSERT INTO customer_work_info (customer_id, full_name, subscription_date, website, work_phnum, work_email) VALUES (%s, %s, %s, %s, %s, %s)"),
        [row['Customer Id'], row['full_name'], row['Subscription Date'], row['Website'], row['Phone 2'], row['work_email']]
    )


conn.commit()
cur.close()
conn.close()

print("Data has been successfully inserted into the database.")
