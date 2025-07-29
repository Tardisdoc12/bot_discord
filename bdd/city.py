################################################################################
# filename: city.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 29/07,2025
################################################################################

import sqlite3

################################################################################

base_de_donnees_path = "bdds/jobs.db"

################################################################################

def get_cities_from_user_id(user_id : int) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT city FROM cities WHERE user_id = ?", (user_id,))
    cities = cursor.fetchall()
    conn.close()
    return cities

################################################################################

def add_city(user_id : int, city : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cities (user_id, city) VALUES (?, ?)", (user_id, city))
    conn.commit()
    conn.close()

################################################################################

def delete_city(user_id : int, city : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cities WHERE user_id = ? AND city = ?", (user_id, city))
    conn.commit()
    conn.close()

################################################################################

def update_city(user_id : int, old_city : str, new_city : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE cities SET city = ? WHERE user_id = ? AND city = ?", (new_city, user_id, old_city))
    conn.commit()
    conn.close()

################################################################################
# End of File
################################################################################