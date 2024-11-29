import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname="ford_workshop",
        user="admin",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Створення таблиць
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Clients (
        client_id SERIAL PRIMARY KEY,
        company_name VARCHAR(100) NOT NULL,
        bank_account VARCHAR(20) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        contact_person VARCHAR(50),
        address TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Cars (
        car_id SERIAL PRIMARY KEY,
        brand VARCHAR(20) CHECK (brand IN ('Fiesta', 'Focus', 'Fusion', 'Mondeo')),
        price DECIMAL(10, 2) NOT NULL,
        client_id INT REFERENCES Clients(client_id) ON DELETE CASCADE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Repairs (
        repair_id SERIAL PRIMARY KEY,
        start_date DATE NOT NULL,
        car_id INT REFERENCES Cars(car_id) ON DELETE CASCADE,
        repair_type VARCHAR(20) CHECK (repair_type IN ('Warranty', 'Scheduled', 'Overhaul')),
        hourly_rate DECIMAL(10, 2) NOT NULL,
        discount DECIMAL(5, 2) CHECK (discount BETWEEN 0 AND 10),
        hours_required INT NOT NULL
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()
