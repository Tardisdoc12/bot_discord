################################################################################
# filename: tags_bdd.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 23/07,2025
################################################################################

import sqlite3

################################################################################

base_de_donnees_path = "bdds/jobs.db"
tags = [
    "AI",
    "Machine Learning",
    "Deep Learning",
    "Frontend",
    "Backend",
    "AdminSys",
    "Cybersecurity",
    "Data Science",
    "Full Stack",
    "Full Time",
    "Part Time",
    "Remote",
    "On-Site",
    "Hybrid",
    "Internship",
    "Junior",
    "Senior",
    "Manager",
    "C",
    "C#",
    "Rust",
    "Assembly",
    "C++",
    "Python",
    "Java",
    "JavaScript",
    "OpenGL",
    "React",
    "HTML",
    "CSS",
    "SQL",
    "NoSQL",
    "Git",
    "GitHub",
    "Mercurial",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Windows",
    "MacOS",
    "Unix",
    "Linux",
]

################################################################################

def get_tags_from_user_id(user_id : int) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags_user WHERE user_id = ?", (user_id,))
    tags = cursor.fetchall()
    tags = [tag[0] for tag in tags if tag is not None]
    conn.close()
    return tags

################################################################################

def get_tags_from_user_name(user_name : str) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags_user INNER JOIN users ON tags_user.user_id = users.user_id WHERE user_name = ?", (user_name,))
    tags = cursor.fetchall()
    tags = list(set([tag[0] for tag in tags if tag is not None]))
    conn.close()
    return tags

################################################################################

def get_all_tags() -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tag FROM tags_user")
    tags = list(cursor.fetchall())
    tags = ", ".join(tags)
    conn.close()
    return tags

################################################################################

def get_users_from_tag(tag : str) -> list:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name FROM users INNER JOIN tags_user ON tags_user.user_id = users.user_id WHERE tag = ?", (tag,))
    users = cursor.fetchall()
    users = list(set([user[0] for user in users if user is not None]))
    conn.close()
    return users

################################################################################

def add_tag_to_user(user_id : int, tag : str) -> None:
    tags = get_tags_from_user_id(user_id)
    if tag in tags:
        return
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tags_user (user_id, tag) VALUES (?, ?)", (user_id, tag))
    conn.commit()
    conn.close()

################################################################################

def delete_tag_user_id(user_id : int, tag : str) -> None:
    conn = sqlite3.connect(base_de_donnees_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tags_user WHERE user_id = ? AND tag = ?", (user_id, tag))
    conn.commit()
    conn.close()

################################################################################
# End of File
################################################################################