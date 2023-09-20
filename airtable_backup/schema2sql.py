import json
import sqlite3
import csv

# Load schema
with open('schema.json') as f:
    schema = json.load(f)

# Connect to SQLite database
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create table for each schema table
for table in schema:
    table_name = table['id']
    fields = [(f['id'], f['type']) for f in table['fields']]
    
    c.execute(f'''CREATE TABLE {table_name} 
                ({', '.join([f[0] + ' ' + f[1] for f in fields])})''')

# Load data from CSVs 
for table in schema:
    table_name = table['id']
    csv_file = table_name + '.csv'
    
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        
        insert_stmt = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['?' for _ in cols])})"
        
        for row in reader:
            values = [row[col] for col in cols]
            c.execute(insert_stmt, values)
            
conn.commit()
conn.close()
