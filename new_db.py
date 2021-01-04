from server import db
import os

os.remove("sensor_value.db")
db.create_all()