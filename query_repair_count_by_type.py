import psycopg2

def repair_count_by_type():
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    print("Кількість кожного типу ремонту для кожного клієнта:")
    cur.execute("""
    SELECT Clients.company_name, Repairs.repair_type, COUNT(*) AS repair_count
    FROM Repairs
    JOIN Cars ON Repairs.car_id = Cars.car_id
    JOIN Clients ON Cars.client_id = Clients.client_id
    GROUP BY Clients.company_name, Repairs.repair_type
    ORDER BY Clients.company_name, Repairs.repair_type;
    """)
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    repair_count_by_type()
