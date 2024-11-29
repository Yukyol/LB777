import psycopg2

def repair_count_by_brand():
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    print("Кількість ремонтів для кожної марки автомобіля:")
    cur.execute("""
    SELECT Cars.brand, COUNT(*) AS repair_count
    FROM Repairs
    JOIN Cars ON Repairs.car_id = Cars.car_id
    GROUP BY Cars.brand
    ORDER BY Cars.brand;
    """)
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    repair_count_by_brand()
