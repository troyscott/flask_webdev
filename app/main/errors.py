from flask import render_template
from . import main

# @app.errorhanler only supports the the main Blueprint
# use app_errorhandler for application level error handling
@main.app_errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

