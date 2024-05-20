""" Create all tables
Seed database with configuration data from TMDB API. Do this you need run flask shell command. From there import seed.py like this: import app.seed as seed. From there run the function to seed database table. EX: seed.fill_country_table()
"""

from app import db
from app.models import Country
import app.api as api

##### Filling the Country table ######################

def fill_country_table():
    countries = api.all_countries()
    for country in countries:
        db.session.add(Country(
            id = country['iso_3166_1'],
            name = country['native_name']
            ))
    db.session.commit()
########################################################

