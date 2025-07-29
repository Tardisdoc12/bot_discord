################################################################################
# filename: urls.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import sqlite3

from bdd.users import get_user_id_from_user_name

################################################################################

base_de_donnees_path = "/mount/bdd/jobs.db"

################################################################################

def get_urls_from_user_id(id : int) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls WHERE user_id = ?", (id,))
    urls = cursor.fetchall()
    conn.close()
    return urls

################################################################################

def get_urls_from_user_name(user_name : str) -> list:
    id = get_user_id_from_user_name(user_name)
    if id is None:
        return None
    urls = get_urls_from_user_id(id[0])
    return urls

################################################################################

def verify_url_exists(id : int, url : str) -> bool:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM urls WHERE user_id = ? AND url = ?", (id, url))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    return True

################################################################################

def add_url(id : int, url : str) -> None:
    if verify_url_exists(id, url):
        return
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (user_id, url) VALUES (?, ?)", (id, url))
    conn.commit()
    conn.close()

################################################################################

def delete_url(id : int, url : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE user_id = ? AND url = ?", (id, url))
    conn.commit()
    conn.close()

################################################################################

def update_url(id : int, old_url : str, new_url : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE urls SET url = ? WHERE user_id = ? AND url = ?", (new_url, id, old_url))
    conn.commit()
    conn.close()

################################################################################
# End of File
################################################################################