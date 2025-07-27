################################################################################
# filename: users.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import sqlite3

################################################################################

base_de_donnees_path = "bdds/jobs.db"

################################################################################

def add_user(user_id : int, user_name : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
    conn.commit()
    conn.close()

################################################################################

def get_user_name_from_user_id(user_id: int) -> str:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM users WHERE user_id = ?", (user_id,))
    user_name = cursor.fetchone()
    conn.close()
    return user_name

################################################################################

def get_user_id_from_user_name(user_name : str) -> int:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_name = ?", (user_name,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id

################################################################################

def update_profil_user(user_id : int):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET profil_created = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

################################################################################

def get_profil_already_created(user_id : int) -> bool:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT profil_created FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    if result[0] == 0:
        return False
    return True

################################################################################

def verify_user_already_exist(user_id : int) -> bool:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    return True

################################################################################
# End of File
################################################################################