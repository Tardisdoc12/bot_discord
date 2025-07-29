################################################################################
# filename: tags_jobs.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

import sqlite3

################################################################################

base_de_donnees_path = "/mount/bdd/jobs.db"

################################################################################

def add_tag_job(tag, job_id):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tags_jobs (tag, job_id) VALUES (?, ?)", (tag, job_id))
    conn.commit()
    conn.close()

################################################################################

def all_tags_job(job_id : int):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags_jobs WHERE job_id = ?", (job_id,))
    tags = cursor.fetchall()
    tags = [tag[0] for tag in tags if tag is not None]
    conn.close()
    return tags

################################################################################

def all_jobs_tag(tag : str):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT jobs.id,title,company,description,user_id,url,salaire,horaires FROM jobs INNER JOIN tags_jobs ON jobs.id = tags_jobs.job_id WHERE tag = ?", (tag,))
    jobs = cursor.fetchall()
    conn.close()
    return jobs

################################################################################

def delete_tag_job(tag, job_id):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tags_jobs WHERE tag = ? AND job_id = ?", (tag, job_id))
    conn.commit()
    conn.close()

################################################################################

def delete_all_tags_job(job_id):
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tags_jobs WHERE job_id = ?", (job_id,))
    conn.commit()
    conn.close()

################################################################################
# End of File
################################################################################