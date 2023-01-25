from pyfladesk import init_gui
from flask import Flask
import logging


app = Flask(__name__)
app.logger.setLevel(logging.CRITICAL)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1
log = logging.getLogger('werkzeug') 
log.setLevel(logging.ERROR)

from routes import *

if __name__ == '__main__':
   init_gui(app, icon="static/images/icons/atom-beta.ico", width=1440, height=720, window_title="Dousojin")
