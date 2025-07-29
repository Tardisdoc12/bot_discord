################################################################################
# filename: gestion_bdd.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################

import sqlite3

################################################################################

base_de_donnees_path = "/mount/bdd/jobs.db"

################################################################################

def get_user_cv_path(id : int) -> str:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT chemin FROM resume WHERE user_id = ?", (id,))
    chemin = cursor.fetchone()
    conn.close()
    return chemin

################################################################################

def get_user_cv_path_from_name(name : str) -> str:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT chemin FROM resume INNER JOIN users ON resume.user_id = users.user_id WHERE user_name = ?", (name,))
    chemin = cursor.fetchone()
    conn.close()
    return chemin

################################################################################

def create_user_cv_path(user_id : int, chemin : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resume (user_id, chemin) VALUES (?, ?)", (user_id, chemin))
    conn.commit()
    conn.close()

################################################################################

def update_user_cv_path(id : int, chemin : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE resume SET chemin = ? WHERE user_id = ?", (chemin, id))
    conn.commit()
    conn.close()

################################################################################

def delete_user_cv_path(id : int) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resume WHERE user_id = ?", (id,))
    conn.commit()
    conn.close()

################################################################################

def verify_user_already_exist(id : int) -> bool:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resume WHERE user_id = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    return True

################################################################################
# End of File
################################################################################