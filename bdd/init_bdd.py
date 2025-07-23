################################################################################
# filename: init_bdd.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################

import os

import sqlite3

################################################################################
def init_db():
    base_de_donnees_path = "bdds"
    if not os.path.exists(base_de_donnees_path):
        os.mkdir(base_de_donnees_path)

    conn = sqlite3.connect(base_de_donnees_path + "/" + "jobs.db")
    cursor = conn.cursor()

    ################################################################################

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_resume (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemin TEXT NOT NULL,
        user_id TEXT NOT NULL,
        user_name TEXT NOT NULL
    )
    """)
    conn.commit()

    ################################################################################

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recruiter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemin TEXT NOT NULL,
        user_id TEXT NOT NULL,
        company TEXT NOT NULL
    )
    """)

    ################################################################################

    conn.commit()

    ################################################################################

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tags TEXT NOT NULL,
        user_id TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user_resume(user_id)
    )
    """)

    ################################################################################

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée.")


################################################################################
# End of File
################################################################################