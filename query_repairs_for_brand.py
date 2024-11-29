import psycopg2

def repairs_for_brand(brand):
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    print(f"Ремонти для марки {brand}:")
    cur.execute("""
    SELECT * 
    FROM Repairs
    JOIN Cars ON Repairs.car_id = Cars.car_id
    WHERE Cars.brand = %s;
    """, (brand,))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    brand = input("Введіть марку авто (наприклад, 'Focus'): ")
    repairs_for_brand(brand)
