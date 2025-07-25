################################################################################
# filename: tags_jobs.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

from bdd.tags_jobs import (
    add_tag_job,
    all_tags_job,
    all_jobs_tag,
    delete_tag_job,
    delete_all_tags_job
)

################################################################################

def add_tag_to_job(tag : str, job_id : int):
    add_tag_job(tag, job_id)
    return f"Tag {tag} added to job"

################################################################################

def get_all_tags_job(job_id : int):
    tags = all_tags_job(job_id)
    return tags

################################################################################

def get_jobs_from_tag(tag : str):
    jobs = all_jobs_tag(tag)
    return jobs

################################################################################

def delete_tag_from_job(tag : str, job_id : int):
    delete_tag_job(tag, job_id)
    return f"Tag {tag} deleted from job"

################################################################################

def delete_all_tags_from_job(job_id : int):
    delete_all_tags_job(job_id)
    return f"All tags deleted from job"

################################################################################
# End of File
################################################################################