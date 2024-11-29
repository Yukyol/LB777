import psycopg2

def insert_data():
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Вставка даних у таблицю Clients
    cur.execute("""
    INSERT INTO Clients (company_name, bank_account, phone, contact_person, address)
    VALUES
        ('ABC Ltd', '1234567890', '380501234567', 'John Doe', 'Kyiv, Ukraine'),
        ('Best Cars', '0987654321', '380671234567', 'Jane Roe', 'Lviv, Ukraine'),
        ('Clever Mechanics', '1122334455', '380981234567', 'Paul Smith', 'Odesa, Ukraine'),
        ('Drive Auto', '6677889900', '380631234567', 'Anna Taylor', 'Dnipro, Ukraine'),
        ('Eco Motors', '5566778899', '380441234567', 'Mark Wilson', 'Kharkiv, Ukraine'),
        ('Future Cars', '9988776655', '380931234567', 'Emma Brown', 'Zaporizhzhia, Ukraine');
    """)

    # Вставка даних у таблицю Cars
    cur.execute("""
    INSERT INTO Cars (brand, price, client_id)
    VALUES
        ('Fiesta', 15000, 1),
        ('Focus', 20000, 2),
        ('Fusion', 18000, 3),
        ('Mondeo', 25000, 4);
    """)

    # Вставка даних у таблицю Repairs
    cur.execute("""
    INSERT INTO Repairs (start_date, car_id, repair_type, hourly_rate, discount, hours_required)
    VALUES
        ('2024-01-15', 1, 'Warranty', 50, 5, 10),
        ('2024-02-10', 2, 'Scheduled', 40, 0, 8),
        ('2024-03-05', 3, 'Overhaul', 60, 10, 15),
        ('2024-03-10', 4, 'Warranty', 50, 7, 12);
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    insert_data()
