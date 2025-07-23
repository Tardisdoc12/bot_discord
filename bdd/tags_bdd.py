################################################################################
# filename: tags_bdd.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################

import sqlite3

################################################################################

base_de_donnees_path = "bdds/jobs.db"

################################################################################

def get_tags_from_user_id(user_id : int) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags WHERE user_id = ?", (user_id,))
    tags = cursor.fetchall()
    conn.close()
    return tags

################################################################################

def get_tags_from_user_name(user_name : str) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags INNER JOIN user_resume ON tags.user_id = user_resume.id WHERE user_name = ?", (user_name,))
    tags = cursor.fetchall()
    conn.close()
    return tags

################################################################################

def get_all_tags() -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags")
    tags = cursor.fetchall()
    conn.close()
    return tags

################################################################################
# End of File
################################################################################