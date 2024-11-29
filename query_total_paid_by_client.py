import psycopg2

def total_paid_by_client():
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    print("Загальна сума, яку сплатив кожен клієнт:")
    cur.execute("""
    SELECT Clients.company_name, SUM(hourly_rate * hours_required * (1 - discount / 100)) AS total_paid
    FROM Repairs
    JOIN Cars ON Repairs.car_id = Cars.car_id
    JOIN Clients ON Cars.client_id = Clients.client_id
    GROUP BY Clients.company_name;
    """)
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    total_paid_by_client()
