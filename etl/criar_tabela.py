import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="lab",
    user="admin",
    password="admin123"
)

cur = conn.cursor()

# Execute SQL from sql/create_tables.sql
with open('sql/create_tables.sql', 'r') as f:
    sql_script = f.read()
    cur.execute(sql_script)

conn.commit()

cur.close()
conn.close()

print("Tabela criada com sucesso!")