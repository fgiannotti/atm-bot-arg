from atmfinder.models import ATM
import psycopg2
from psycopg2 import sql


def search_by_network(lat:float, long:float, network:str)->[ATM]:
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
        ) * 6371 * 2 * 1000 as distance, banco, ubicacion, lat, long  from "cajeros-automaticos" as caj 
        where red=%s AND asin(
          sqrt(
            sin(radians(caj.lat-%s)/2)^2 +
            sin(radians(caj.long-%s)/2)^2 *
            cos(radians(%s)) *
            cos(radians(%s))
              )
        ) * 6371 * 2 * 1000 <= 500 order by distance asc limit 3 """),[lat,long,lat,long,network,lat,long,lat,long])

        rows = cursor.fetchall()
        print(rows)

        for row in rows:
            atm = ATM(name=row[1],address=row[2],dist=row[0],lat=row[3],long=row[4])
            atms.append(atm)
    except (Exception, psycopg2.Error) as error:
        print("[DAO][SearchByNetwork] Error while fetching data from PostgreSQL", error)
        raise
    
    return atms
  
  
def get_network_chosen_for_user(chatID: int):
    ok = True
    network = "no-network"

    try:
        db = psycopg2.connect(dbname="dehk8k9ckm1b5r", user="ulnxxperftvpyj", password="9d6f464e63dc1b36466508b5a2d1c2b8cb172e20bc29677fd4556940491b7dc3", host="ec2-18-214-208-89.compute-1.amazonaws.com")
        cursor = db.cursor()
        query = "select network from \"users\" where chat_id={} order by id desc".format(chatID)
        print(query)
        cursor.execute(query)
        network = cursor.fetchone()[0]

    except (Exception, psycopg2.Error) as error:
        print("[DAO][get_network_chosen_for_user] Error while fetching data from PostgreSQL", error)
        ok = False

    finally:
        # closing database connection.
        if db:
            cursor.close()
            db.close()
            print("[DAO][get_network_chosen_for_user] PostgreSQL connection is closed")

    return ok, network


def set_network_chosen_for_user(network: str, chatID:int):

    try:
        db = psycopg2.connect(dbname="dehk8k9ckm1b5r", user="ulnxxperftvpyj", password="9d6f464e63dc1b36466508b5a2d1c2b8cb172e20bc29677fd4556940491b7dc3", host="ec2-18-214-208-89.compute-1.amazonaws.com")
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (chat_id, network) VALUES (%s, %s);", chatID, network)
        network = cursor.fetchone()[0]

    except (Exception, psycopg2.Error) as error:
        print("[DAO][set_network_chosen_for_user] Error while fetching data from PostgreSQL", error)
        raise

    finally:
        # closing database connection.
        if db:
            cursor.close()
            db.close()
            print("[DAO][set_network_chosen_for_user] PostgreSQL connection is closed")

    return

