################################################################################
# filename: city_user.py
# Author: Jean Anquetil
# Email: janquetil@e-vitech.com
# Date: 29/07,2025
################################################################################

from bdd.city import (
    add_city,
    delete_city,
    update_city,
    get_cities_from_user_id,
    get_cities_from_user_name
)

################################################################################

def get_city_from_user_id(user_id : int) -> list:
    cities = get_cities_from_user_id(user_id)
    if len(cities) == 0:
        return []
    return cities[0]

################################################################################

def get_city_from_user_name(user_name : str) -> list:
    cities = get_cities_from_user_name(user_name)
    return cities

################################################################################

def verif_city_already_link(user_id: int) -> bool:
    cities = get_cities_from_user_id(user_id)
    if len(cities) == 0:
        return False
    return True

################################################################################

def add_city_to_user(user_id : int, city : str) -> None:
    if verif_city_already_link(user_id):
        return False
    add_city(user_id, city)
    return True

################################################################################

def delete_city_from_user(user_id : int, city : str) -> None:
    if not verif_city_already_link(user_id):
        return False
    delete_city(user_id, city)
    return True

################################################################################

def update_city_from_user(user_id : int, old_city : str, new_city : str) -> None:
    if not verif_city_already_link(user_id):
        return False
    update_city(user_id, old_city, new_city)
    return True

################################################################################
# End of File
################################################################################