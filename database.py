import sqlite3
import hashlib
from datetime import datetime, timedelta

DB_NAME = "bot_ad.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identificacion TEXT UNIQUE,
        nombre TEXT,
        usuario TEXT UNIQUE,
        clave TEXT,
        correo TEXT,
        fecha_nacimiento TEXT,
        fecha_inicio TEXT,
        fecha_final TEXT,
        perfil TEXT,
        numero_ingresos INTEGER DEFAULT 0,
        analisis_realizados INTEGER DEFAULT 0,
        estado TEXT DEFAULT 'pendiente',
        membresia TEXT DEFAULT 'gratis'
    )''')
    
    # Migración para bases de datos viejas (añade la columna nombre si no existe)
    try:
        c.execute("ALTER TABLE users ADD COLUMN nombre TEXT")
    except sqlite3.OperationalError:
        pass
        
    c.execute("SELECT * FROM users WHERE usuario='dasb1512'")
    if not c.fetchone():
        hashed_pw = hashlib.sha256("1234567890".encode()).hexdigest()
        today = datetime.now().strftime("%Y-%m-%d")
        c.execute('''INSERT INTO users 
            (identificacion, nombre, usuario, clave, correo, fecha_nacimiento, fecha_inicio, fecha_final, perfil, estado, membresia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            ('8642239', 'Efraneo', 'dasb1512', hashed_pw, 'efraneo@gmail.com', '1976-09-19', today, 'NA', 'administrador', 'aprobado', 'paga'))
        conn.commit()
    conn.close()

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()

def register_user(identificacion, nombre, usuario, clave, correo, fecha_nac):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        end_trial = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        c.execute('''INSERT INTO users 
            (identificacion, nombre, usuario, clave, correo, fecha_nacimiento, fecha_inicio, fecha_final, perfil, estado, membresia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (identificacion, nombre, usuario, hash_password(clave), correo, fecha_nac, today, end_trial, 'usuario', 'pendiente', 'gratis'))
        conn.commit(); return True
    except sqlite3.IntegrityError: return False
    finally: conn.close()

def verify_login(usuario, clave):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE usuario=? AND clave=?", (usuario, hash_password(clave)))
    user = c.fetchone(); conn.close(); return user

def get_email_by_user_id(identificacion, usuario):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT correo FROM users WHERE identificacion=? AND usuario=?", (identificacion, usuario))
    result = c.fetchone(); conn.close()
    return result[0] if result else None

def update_password(identificacion, new_password):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("UPDATE users SET clave=? WHERE identificacion=?", (hash_password(new_password), identificacion))
    conn.commit(); conn.close()

def update_login_stats(usuario):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("UPDATE users SET numero_ingresos = numero_ingresos + 1 WHERE usuario=?", (usuario,))
    conn.commit(); conn.close()

def increment_analysis(usuario):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("UPDATE users SET analisis_realizados = analisis_realizados + 1 WHERE usuario=?", (usuario,))
    conn.commit(); conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT identificacion, nombre, usuario, correo, fecha_inicio, fecha_final, perfil, numero_ingresos, analisis_realizados, estado, membresia FROM users")
    users = c.fetchall(); conn.close(); return users

def update_user(identificacion, nombre, usuario, correo, fecha_final, estado, membresia):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute('''UPDATE users SET 
                 nombre=?, usuario=?, correo=?, fecha_final=?, estado=?, membresia=? 
                 WHERE identificacion=?''', 
                 (nombre, usuario, correo, fecha_final, estado, membresia, identificacion))
    conn.commit(); conn.close()

def delete_user(identificacion):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("DELETE FROM users WHERE identificacion=?", (identificacion,))
    conn.commit(); conn.close()

def approve_user(identificacion, approve=True):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    estado = 'aprobado' if approve else 'rechazado'
    c.execute("UPDATE users SET estado=? WHERE identificacion=?", (estado, identificacion))
    conn.commit(); conn.close()

def update_membership(identificacion, days=30):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    new_end = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    c.execute("UPDATE users SET membresia='paga', fecha_final=?, estado='aprobado' WHERE identificacion=?", (new_end, identificacion))
    conn.commit(); conn.close()

def get_user_by_id(identificacion):
    conn = sqlite3.connect(DB_NAME); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE identificacion=?", (identificacion,))
    user = c.fetchone(); conn.close(); return user
