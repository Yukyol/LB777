import psycopg2
from psycopg2 import sql


def execute_query(cur, query, params=None):
    """Виконує SQL-запит і повертає результат."""
    cur.execute(query, params or ())
    return cur.fetchall()


def print_table(cur, table_name):
    """Друкує вміст таблиці."""
    print(f"\n--- Вміст таблиці: {table_name} ---")
    cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
    rows = cur.fetchall()
    if rows:
        # Отримання назв стовпців
        col_names = [desc[0] for desc in cur.description]
        print(f"{' | '.join(col_names)}")
        print("-" * (len(' | '.join(col_names)) + 10))
        # Вивід рядків
        for row in rows:
            print(" | ".join(map(str, row)))
    else:
        print(f"Таблиця '{table_name}' порожня.")


def show_all_tables_and_queries():
    # Параметри підключення до бази даних
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    try:
        # Отримання списку таблиць
        cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
        """)
        tables = cur.fetchall()

        if not tables:
            print("У базі даних немає таблиць.")
            return

        # Вивід таблиць
        for table in tables:
            print_table(cur, table[0])

        # Виконання запитів
        print("\n--- Виконання запитів ---")

        # 1. Відобразити інформацію про всі гарантійні ремонти, відсортувати назви клієнтів
        query1 = """
        SELECT cl.company_name, r.* 
        FROM repairs r
        JOIN cars c ON r.car_id = c.car_id
        JOIN clients cl ON c.client_id = cl.client_id
        WHERE r.repair_type = 'гарантійний'
        ORDER BY cl.company_name;
        """
        print("\n1. Інформація про всі гарантійні ремонти (відсортовано):")
        results = execute_query(cur, query1)
        for row in results:
            print(row)

        # 2. Порахувати вартість ремонту та вартість з урахуванням знижки
        query2 = """
        SELECT c.brand, 
               r.hours_required * r.hourly_rate AS total_cost,
               (r.hours_required * r.hourly_rate) * (1 - r.discount / 100.0) AS discounted_cost
        FROM repairs r
        JOIN cars c ON r.car_id = c.car_id;
        """
        print("\n2. Вартість ремонту та вартість зі знижкою:")
        results = execute_query(cur, query2)
        for row in results:
            print(row)

        # 3. Інформація по ремонту для авто заданої марки
        query3 = """
        SELECT * 
        FROM repairs r
        JOIN cars c ON r.car_id = c.car_id
        WHERE c.brand = %s;
        """
        brand = "Fiesta"  # Змініть на потрібну марку
        print(f"\n3. Інформація про ремонти для марки '{brand}':")
        results = execute_query(cur, query3, (brand,))
        for row in results:
            print(row)

        # 4. Загальна сума, яку сплатив кожен клієнт
        query4 = """
        SELECT cl.company_name, 
               SUM(r.hours_required * r.hourly_rate * (1 - r.discount / 100.0)) AS total_paid
        FROM repairs r
        JOIN cars c ON r.car_id = c.car_id
        JOIN clients cl ON c.client_id = cl.client_id
        GROUP BY cl.company_name;
        """
        print("\n4. Загальна сума, сплачена кожним клієнтом:")
        results = execute_query(cur, query4)
        for row in results:
            print(row)

        # 5. Кількість кожного типу ремонту для кожного клієнта
        query5 = """
        SELECT cl.company_name, r.repair_type, COUNT(*) AS count_repairs
        FROM repairs r
        JOIN cars c ON r.car_id = c.car_id
        JOIN clients cl ON c.client_id = cl.client_id
        GROUP BY cl.company_name, r.repair_type;
        """
        print("\n5. Кількість кожного типу ремонту для кожного клієнта:")
        results = execute_query(cur, query5)
        for row in results:
            print(row)

        # 6. Кількість ремонтів для кожної марки автомобіля
        query6 = """
        SELECT c.brand, COUNT(*) AS count_repairs
        FROM repairs r
        JOIN cars c ON r.car_id = c.car_id
        GROUP BY c.brand;
        """
        print("\n6. Кількість ремонтів для кожної марки автомобіля:")
        results = execute_query(cur, query6)
        for row in results:
            print(row)

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    show_all_tables_and_queries()
