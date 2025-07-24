################################################################################
# filename: jobs.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import sqlite3

################################################################################

base_de_donnees_path = "bdds/jobs.db"

################################################################################

def get_jobs_from_title(title : str):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE title = ?", (title,))
    jobs = cursor.fetchall()
    conn.close()
    return jobs

################################################################################

def get_jobs_from_company(company : str):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE company = ?", (company,))
    jobs = cursor.fetchall()
    conn.close()
    return jobs

################################################################################

def create_jobs(title : str, company : str, description : str, link : str, user_id : int) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, company, description, url, user_id) VALUES (?, ?, ?, ?)", (title, company, description, link, user_id))
    conn.commit()
    conn.close()

################################################################################

def get_all_jobs_from_user_id(user_id : int) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, description FROM jobs WHERE user_id = ?", (user_id,))
    jobs = cursor.fetchall()
    jobs = [job[0] for job in jobs if job is not None]
    conn.close()
    return jobs

################################################################################

def get_all_jobs_from_user_name(user_name : str) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, company, description FROM jobs INNER JOIN users ON jobs.user_id = users.user_id WHERE user_name = ?", (user_name,))
    jobs = cursor.fetchall()
    jobs = [job[0] for job in jobs if job is not None]
    conn.close()
    return jobs

################################################################################

def delete_job(job_id : int) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()

################################################################################

def get_job_id_from_title(title : str) -> int:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jobs WHERE title = ?", (title,))
    job_id = cursor.fetchone()[0]
    conn.close()
    return job_id

################################################################################
# End of File
################################################################################