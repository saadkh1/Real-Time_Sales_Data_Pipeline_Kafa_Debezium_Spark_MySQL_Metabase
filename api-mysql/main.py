from flask import Flask
import mysql.connector
import random
from datetime import datetime
import time

app = Flask(__name__)

Articles = {
    "Croissant": 1.5,
    "Chocolate Eclair": 7.5,
    "Fruit Tart": 8.5,
    "Cinnamon Roll": 4.0,
    "Danish Pastry": 6.5,
    "Palmier": 3.0,
    "Cream Puff": 9.0,
    "Apple Turnover": 5.0,
    "Bear Claw": 6.8,
    "Napoleon": 7.9,
    "Cheesecake": 10.5,
    "Strudel": 8.0,
    "Muffin": 3.5,
    "Baguette": 2.0,
    "Scone": 2.8,
    "Cupcake": 4.5,
    "Cherry Pie": 9.5,
    "Blueberry Muffin": 3.8,
    "Pecan Pie": 11.0,
    "Key Lime Tart": 8.2,
    "Red Velvet Cake": 12.0,
    "Lemon Bar": 6.0
}

databases = {
    "mysql_1": {"host": "Jendouba_Host", "location": "jendouba", "pos_id": 1, "latitude": "36.499043885304644", "longitude": "8.774471269751299"},
    "mysql_2": {"host": "Beja_Host", "location": "beja", "pos_id": 2, "latitude": "36.72781814215737", "longitude": "9.185413567546759"},
    "mysql_3": {"host": "Kef_Host", "location": "kef", "pos_id": 3, "latitude": "36.1703408760811", "longitude": "8.697009708310699"}
}

def insert_data_to_database():
    while True:
        database = random.choice(list(databases.keys()))
        mydb = mysql.connector.connect(
            host=databases[database]["host"],
            user="root",
            password="secret",
            database=databases[database]["location"] + "_sales_db"
        )
        cursor = mydb.cursor()

        article = random.choice(list(Articles.keys()))
        prix = Articles[article]

        quantity = random.choice(list(range(1, 20)))
        total = quantity * prix

        sale_type = random.choice(["direct", "livraison"])
        payment_mode = "online" if sale_type == "livraison" else random.choice(["cash", "card"])

        sale_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        location = databases[database]["location"]
        pos_id = databases[database]["pos_id"]

        latitude = databases[database]["latitude"]
        longitude = databases[database]["longitude"]
        
        table_name = databases[database]["location"] + "_sales"

        sql = "INSERT INTO {} (pos_id, pos_name, article, quantity, unit_price, total, sale_type, payment_mode, sale_time, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table_name)
        val = (pos_id, location, article, quantity, prix, total, sale_type, payment_mode, sale_time, latitude, longitude)
        cursor.execute(sql, val)
        mydb.commit()

        time_to_sleep = random.randint(1, 4)
        time.sleep(time_to_sleep)

if __name__ == '__main__':
    insert_data_to_database()
    app.run(debug=True, host='0.0.0.0')
