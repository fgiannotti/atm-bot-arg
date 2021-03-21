from atmfinder.models import ATM
import psycopg2
from psycopg2 import sql
def SearchByNetwork(lat:float, long:float, network:str):
    atms = []
    try:
        db = psycopg2.connect(dbname="dehk8k9ckm1b5r", user="ulnxxperftvpyj", password="9d6f464e63dc1b36466508b5a2d1c2b8cb172e20bc29677fd4556940491b7dc3", host="ec2-18-214-208-89.compute-1.amazonaws.com")
        cursor = db.cursor()

        cursor.execute(sql.SQL("""select asin(
          sqrt(
            sin(radians(caj.lat-%s)/2)^2 +
            sin(radians(caj.long-%s)/2)^2 *
            cos(radians(%s)) *
            cos(radians(%s))
              )
        ) * 6371 * 2 as distance, banco,ubicacion  from "cajeros-automaticos" as caj 
        where asin(
          sqrt(
            sin(radians(caj.lat-%s)/2)^2 +
            sin(radians(caj.long-%s)/2)^2 *
            cos(radians(%s)) *
            cos(radians(%s))
              )
        ) * 6371 * 2 <= 0.5 order by distance asc limit 3 """),[lat,long,lat,long,lat,long,lat,long])
        atms = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("[DAO][SearchByNetwork] Error while fetching data from PostgreSQL", error)
    
    return atms
  
  
  
  
  
def SearchAll():
    
    atms = []
    try:
        db = psycopg2.connect(dbname="dehk8k9ckm1b5r", user="ulnxxperftvpyj", password="9d6f464e63dc1b36466508b5a2d1c2b8cb172e20bc29677fd4556940491b7dc3", host="ec2-18-214-208-89.compute-1.amazonaws.com")
        cursor = db.cursor()
        query = "select * from \"cajeros-automaticos\" limit 10"

        cursor.execute(query)
        print("Selecting rows from mobile table using cursor.fetchall")
        atms = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("[DAO][SearchALL] Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if db:
            cursor.close()
            db.close()
            print("[DAO][SearchALL] PostgreSQL connection is closed")
   
    return atms