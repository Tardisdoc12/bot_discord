################################################################################
# filename: urls.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 24/07,2025
################################################################################

from bdd.urls import (
    get_urls_from_user_id,
    get_urls_from_user_name,
    add_url,
    delete_url,
    update_url
)
from bdd.users import get_user_id_from_user_name

################################################################################

def create_url(id : int, url : str) -> None:
    add_url(id, url)

################################################################################

def delete_url_from_user(id : int, url : str) -> None:
    delete_url(id, url)

################################################################################

def update_url_from_user(id : int, old_url : str, new_url : str) -> None:
    update_url(id, old_url, new_url)

################################################################################

def get_urls_from_user(user_id_or_name : str | int) -> list:
    if isinstance(user_id_or_name, str):
        urls = get_urls_from_user_name(user_id_or_name)
    else:
        urls = get_urls_from_user_id(id)
    if urls:
        urls = list(set([url[0] for url in urls if url is not None]))
        return urls
    return []

################################################################################
# End of File
################################################################################