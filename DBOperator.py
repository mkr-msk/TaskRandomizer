import sqlite3

def connect_to_db():
    conn = sqlite3.connect('tr_data.db')
    return conn

def get_all_items():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Elements")
    return cursor.fetchall()

def add_item(item):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Elements (Name, Priority, Active) VALUES (?, ?, ?)",
        (
            item.name,
            item.priority,
            item.active
        )
    )
    conn.commit()

def delete_item(name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Elements WHERE name=?", (name,))
    conn.commit()

def update_item(name, new_value):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Elements SET value=? WHERE name=?", (new_value, name))
    conn.commit()

def search_items(search_term):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Elements WHERE name LIKE ?", ('%' + search_term + '%',))
    return cursor.fetchall()