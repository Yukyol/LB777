import psycopg2

def repair_cost_with_discount():
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    print("Вартість ремонту з урахуванням знижки:")
    cur.execute("""
    SELECT repair_id, (hourly_rate * hours_required) AS total_cost,
           ((hourly_rate * hours_required) * (1 - discount / 100)) AS discounted_cost
    FROM Repairs;
    """)
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    repair_cost_with_discount()
