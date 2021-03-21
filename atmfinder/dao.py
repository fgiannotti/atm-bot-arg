import psycopg2

# Connect to your postgres DB
print("DAO CALLED")

def searchAll():
	
	try:
		db = psycopg2.connect(dbname="dehk8k9ckm1b5r", user="ulnxxperftvpyj", password="9d6f464e63dc1b36466508b5a2d1c2b8cb172e20bc29677fd4556940491b7dc3", host="ec2-18-214-208-89.compute-1.amazonaws.com")
		cursor = DB.cursor()
		query = "select * from cajeros-automaticos top 10"

		cursor.execute(query)
		print("Selecting rows from mobile table using cursor.fetchall")
		atms = cursor.fetchall()

		print("Print each row and it's columns values")
		for row in atms:
			print("asd1 = ", row[0], )
			print("asd2 = ", row[1])
			print("asd3  = ", row[2], "\n")

	except (Exception, psycopg2.Error) as error:
		print("Error while fetching data from PostgreSQL", error)

	finally:
		# closing database connection.
		if connection:
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
   
	return records