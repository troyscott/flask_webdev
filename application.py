import os
from app import create_app

# set the FLASK_CONFIG, default is 'development'
app = create_app(os.getenv('FLASK_CONFIG') or 'default')





