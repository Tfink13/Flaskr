import os

from flask import Flask
# application factory ***
def create_app(test_config=none):
    # create and config application; flask instance 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mappping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # when not testing load the instance config if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed
        app.config.from_mappping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # page says hello
    @app.route('/hello')
    def hello():
        return 'Hello World!'

    return app