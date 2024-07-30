import psycopg2
import csv
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="Newdb",
    user="postgres",
    password="root"
)

cur = conn.cursor()

input_string = input("Enter the string: ").capitalize()

query = """
SELECT
    ci.customer_id,
    cwi.full_name,
    ci.city,
    ci.personal_phnum,
    ci.personal_email,
    cwi.office_loc,
    cwi.subscription_date,
    CURRENT_DATE - cwi.subscription_date AS pending_days,
    cwi.work_phnum,
    cwi.work_email
FROM
    customer_info ci
JOIN
    customer_work_info cwi ON ci.customer_id = cwi.customer_id
WHERE
    cwi.full_name LIKE %s
"""

cur.execute(query, (input_string + '%',))
rows = cur.fetchall()

header = [
    'customer_id',
    'full_name',
    'city',
    'personal_phnum',
    'personal_email',
    'office_loc',
    'subsctiption_date',
    'pending_days',
    'work_phnum',
    'work_email'
]

with open('customer_details.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

print(f"CSV file 'customer_details.csv' generated successfully.")

cur.close()
conn.close()

