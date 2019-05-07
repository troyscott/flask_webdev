import os
from app import create_app


app = create_app(os.getevn('FLASK_CONFIG') or default)





