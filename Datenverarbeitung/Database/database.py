from tinydb import TinyDB, Query
import os

db_connector_temp = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('temperature')

db_connector_blue = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('dispenser_blue')
db_connector_red = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('dispenser_red')
db_connector_green = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('dispenser_green')

db_connector_ground_truth = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('ground_truth')


db_connector_drop_osci = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('drop_oscillation')
