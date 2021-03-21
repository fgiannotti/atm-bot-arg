import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect(dbname="dehk8k9ckm1b5r", user="ulnxxperftvpyj", password="9d6f464e63dc1b36466508b5a2d1c2b8cb172e20bc29677fd4556940491b7dc3", host="ec2-18-214-208-89.compute-1.amazonaws.com")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM my_data")

# Retrieve query results
records = cur.fetchall()