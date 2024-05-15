""" Create all tables
Seed database with configuration data from TMDB API.
"""

from app import db, app
from models import Region
import api

with app.app_context():
    db.drop_all()
    db.create_all()

##### Filling the Region table ######################
regions = api.all_countries()
with app.app_context():
    for region in regions:
        db.session.add(Region(
            id = region['iso_3166_1'],
            name = region['native_name']
            ))
    db.session.commit()
########################################################

