import os
import json
import logging
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_fixtures import load_fixtures
from flask_marshmallow import Marshmallow

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from app import routes, api

models.db.drop_all()
models.db.create_all()
fixture_dir_path = os.path.join('app', 'fixtures')
for fixture in os.listdir(fixture_dir_path):
    fixture_path = os.path.join(fixture_dir_path, fixture)
    with open(fixture_path, 'r') as infile:
        load_fixtures(models.db, json.loads(infile.read()))

if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')