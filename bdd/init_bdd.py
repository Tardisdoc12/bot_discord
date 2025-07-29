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
    base_de_donnees_path = "/mount/bdd"
    if not os.path.exists(base_de_donnees_path):
        os.mkdir(base_de_donnees_path)

    conn = sqlite3.connect(base_de_donnees_path + "/" + "jobs.db")
    cursor = conn.cursor()

    ################################################################################

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_id TEXT NOT NULL,
            profil_created Integer DEFAULT 0
        )
    """)
    conn.commit()

    ################################################################################

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    conn.commit()

    ################################################################################

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chemin TEXT NOT NULL,
        user_id TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)
    conn.commit()

    ################################################################################

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT NOT NULL,
        user_id TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)
    conn.commit()

    ################################################################################

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT NOT NULL,
        job_id TEXT NOT NULL,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )
    """)
    conn.commit()

    ################################################################################

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """
    )

    ################################################################################

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            url TEXT NOT NULL,
            salaire TEXT NOT NULL,
            horaires TEXT NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """
    )

    ################################################################################

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée.")

################################################################################
# End of File
################################################################################