import sqlite3
import random

from Classes import Element


def connect_to_db():
    conn = sqlite3.connect('tr_data.db')

    return conn


def get_token():
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Config")

    return cursor.fetchall()[0][0]


def get_all_items(mode = 'randomized'):
    conn = connect_to_db()
    cursor = conn.cursor()

    if mode == 'sorted':
        cursor.execute(
            "SELECT * \
            FROM Elements \
            ORDER BY \
                Priority DESC, \
                SUBSTR(Name, 1, 1) ASC, \
                Active DESC"
        )

    else:
        cursor.execute(
            "SELECT * \
            FROM Elements \
            ORDER BY RANDOM()"
        )

    return cursor.fetchall()


def add_item(name: str, priority: str, active: str):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute(
        f"INSERT INTO Elements (Name, Priority, Active) \
        VALUES ({name}, {priority}, {active})"
    )

    conn.commit()


def update_item(target, name = '', new_value = ''):
    conn = connect_to_db()
    cursor = conn.cursor()
    if target == 'Name':
        cursor.execute(
            f"UPDATE Elements \
            SET {target} = '{new_value}' \
            WHERE name LIKE '%{name}%'"
        )

    elif target == 'Default':
        cursor.execute(f"UPDATE Elements SET Active = 1")

    else:
        cursor.execute(
            f"UPDATE Elements \
            SET {target} = {new_value} \
            WHERE name LIKE '%{name}%'"
        )

    conn.commit()


def delete_item(name):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM Elements WHERE name LIKE '%{name}%'")

    conn.commit()


def choose_random_element():
    elements = [Element(row[0], row[1], row[2]) for row in get_all_items() if row[2]]

    priority_list = []
    for e in elements:
        for _ in range(e.priority):
            priority_list.append(e.name)

    return random.choice(priority_list)