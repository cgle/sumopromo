from database import metadata
from database.sumodb import SumoDB
from config.db import database_uri, engine_options, session_options

sumo_db = SumoDB(database_uri, metadata=metadata, engine_options=engine_options, session_options=session_options)
sumo_db.drop_all()
sumo_db.create_all()

sumo_db.category.create_from_list(['food drink','restaurant','groceries','bakery','beauty spas','health fitness','salon','gym','travel','pets','retail'])

demo_user = sumo_db.user.add(email='demo@sumo.promo', password='demo', first_name='DEMO', last_name='DEMO')
