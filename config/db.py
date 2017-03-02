__all__ = ('database_uri', 'engine_options', 'session_options',)

database_uri = 'postgres+psycopg2://sumoadmin:adminsumo@localhost:5432/sumodb'
engine_options = {'echo': False, 'encoding': 'utf-8'}
session_options = {}
