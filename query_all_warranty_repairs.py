import psycopg2

def all_warranty_repairs():
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    print("Гарантійні ремонти:")
    cur.execute("""
    SELECT company_name, start_date, repair_type
    FROM Repairs
    JOIN Cars ON Repairs.car_id = Cars.car_id
    JOIN Clients ON Cars.client_id = Clients.client_id
    WHERE repair_type = 'Warranty'
    ORDER BY company_name;
    """)
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    all_warranty_repairs()
