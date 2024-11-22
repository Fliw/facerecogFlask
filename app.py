from flask import Flask, jsonify
from controllers.registerController import register_bp
from controllers.faceTrainController import faceTrain_bp
from controllers.loginController import login_bp
#from controllers.facePredictController import facePredict_bp
from config import Config
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config.from_object(Config)
mysql = MySQL(app)

app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(faceTrain_bp, url_prefix='/faceTrain')
app.register_blueprint(login_bp, url_prefix='/login')
#app.register_blueprint(facePredict_bp, url_prefix='/facePredict')

if __name__ == '__main__':
    app.run(debug=True)
