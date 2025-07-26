################################################################################
# filename: jobs.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

from bdd.jobs import (
    get_jobs_from_title,
    get_jobs_from_company,
    create_jobs,
    get_all_jobs_from_user_id,
    get_all_jobs_from_user_name,
    delete_job,
    get_job_id_from_title,
    get_jobs_id,
    get_job_from_id,
    get_user_id_from_job_id
)

################################################################################

def get_user_from_job_id(job_id : int) -> int:
    user_id = get_user_id_from_job_id(job_id)
    return user_id

################################################################################

def get_job_informations(job_id : int) -> list:
    job = get_job_from_id(job_id)
    return job

################################################################################

def get_job_title(title : str) -> list:
    jobs = get_jobs_from_title(title)
    jobs = [job[0] for job in jobs if job is not None]
    return jobs

################################################################################

def get_job_id(title : str, description : str, company : str, link : str, user_id : int) -> int:
    job_id = get_jobs_id(title, description, company, link, user_id)
    return job_id

################################################################################

def get_job_company(company : str) -> list:
    jobs = get_jobs_from_company(company)
    jobs = [job[0] for job in jobs if job is not None]
    return jobs

################################################################################

def create_job(title : str, company : str, description : str, link : str, user_id : int, salaire : str, horaires : str) -> None:
    create_jobs(title, company, description, link, user_id, salaire, horaires)

################################################################################

def get_all_jobs_user_id(user_id : int) -> list:
    jobs = get_all_jobs_from_user_id(user_id)
    return jobs

################################################################################

def get_all_jobs_user_name(user_name : str) -> list:
    jobs = get_all_jobs_from_user_name(user_name)
    return jobs

################################################################################

def delete_job_by_title(title : str) -> None:
    job_id = get_job_id_from_title(title)
    delete_job(job_id)

################################################################################

def delete_job_by_id(job_id : int) -> None:
    delete_job(job_id)

################################################################################
# End of File
################################################################################