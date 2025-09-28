################################################################################
# filename: migrations.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 28/09,2025
################################################################################

from bdd.tags_users_bdd import *
from bdd.resume_bdd import *
from bdd.urls import *
from bdd.users import *
from bdd.city import *
import logging

################################################################################
logging.basicConfig(level=logging.INFO)

################################################################################


def migration_data(user_name, new_user_id, new_user_name):
    logging.info(f"on a les types : {type(user_name)}, {type(new_user_id)}, {type(new_user_name)}")
    #User A Informations
    try:
        user_id = get_user_id_from_user_name(user_name)[0]
        logging.info(f"on a le type: {type(user_id)}")
        tags = get_tags_from_user_id(user_id)
        urls = get_urls_from_user_id(user_id)
        resume_path = get_user_cv_path_from_name(user_name)
        city = get_cities_from_user_id(user_id)
    except Exception as e:
        logging.info(e)
        return {"success": False, "message": f"Migration echouée : city: {city}, tags: {tags}, urls: {urls}, resume_path: {resume_path}"}
    
    logging.info("on a récupérer les données de l'utilisateur")
    logging.info(f"user_id={user_id}, tags={tags}, urls={urls}, resume_path={resume_path}, city={city}")

    try:
        #User B Informations
        if not verify_user_already_exist(new_user_id):
            add_user(new_user_id, new_user_name)
        for tag in tags:
            add_tag_to_user(new_user_id, tag)
        for url in urls:
            add_url(new_user_id, url)
        if resume_path is not None:
            create_user_cv_path(new_user_id, resume_path[0])
        for city in city:
            add_city(new_user_id, city)
            
        update_profil_user(new_user_id)
    except Exception as e:
        logging.info(e)
        return {"success": False, "message": f"Migration echouée : city: {city}, tags: {tags}, urls: {urls}, resume_path: {resume_path}"}
    return {"success": True, "message": f"Migration effectuée : city: {city}, tags: {tags}, urls: {urls}, resume_path: {resume_path}"}
    

################################################################################
# End of File
################################################################################