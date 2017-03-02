from database import metadata
from database.sumodb import SumoDB
from config.db import database_uri, engine_options, session_options

sumo_db = SumoDB(database_uri, metadata=metadata, engine_options=engine_options, session_options=session_options)
sumo_db.drop_all()
sumo_db.create_all()
