import sqlite3

def create_db():
    con = sqlite3.connect(database=r'tbs.db')
    cur = con.cursor()

    # Empregados
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employee (
        eid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        gender TEXT,
        contact TEXT,
        dob TEXT,
        doj TEXT,
        pass TEXT,
        utype TEXT,
        address TEXT
    )
    """)
    con.commit()

    # Fornecedores
    cur.execute("""
    CREATE TABLE IF NOT EXISTS supplier (
        invoice TEXT PRIMARY KEY,
        name TEXT,
        contact TEXT,
        supdate TEXT,
        valor FLOAT,
        pagamento TEXT,
        datavenc TEXT,
        parcela TEXT,
        observacao TEXT
    )
    """)
    con.commit()

    # Estoque
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        Supplier TEXT,
        itemname TEXT,
        hsncode TEXT,
        price TEXT,
        qty TEXT,
        discount TEXT
    )
    """)
    con.commit()

    # Vendas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sid INTEGER PRIMARY KEY AUTOINCREMENT,
        Sales FLOAT,
        Recebeu FLOAT,
        Troco FLOAT,
        Tipo TEXT,
        Descricao TEXT,
        data DATE,
        hora TIME,
        horaVenda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Pagamento TEXT
    )
    """)
    con.commit()

    con.close()

create_db()
