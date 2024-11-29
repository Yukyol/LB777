import psycopg2
from psycopg2 import sql


def show_all_tables():
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
        # Отримати список усіх таблиць у схемі public
        cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
        """)
        tables = cur.fetchall()

        if not tables:
            print("У базі даних немає таблиць.")
            return

        # Вивести вміст кожної таблиці
        for table in tables:
            table_name = table[0]
            print(f"\n--- Вміст таблиці: {table_name} ---")

            # Динамічний запит для отримання вмісту таблиці
            cur.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            rows = cur.fetchall()

            if rows:
                # Отримання назв стовпців
                col_names = [desc[0] for desc in cur.description]
                # Вивід заголовків таблиці
                print(f"{' | '.join(col_names)}")
                print("-" * (len(' | '.join(col_names)) + 10))

                # Вивід рядків
                for row in rows:
                    print(" | ".join(map(str, row)))
            else:
                print(f"Таблиця '{table_name}' порожня.")

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    show_all_tables()
