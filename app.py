from flask import Flask, jsonify
from controllers.registerController import register_bp
#from controllers.faceTrainController import faceTrain_bp
#from controllers.facePredictController import facePredict_bp
from config import Config
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/test_db', methods=['GET'])
def test_db_connection():
    try:
        # Gunakan cursor default, bukan DictCursor
        cur = mysql.connection.cursor()

        # Jalankan query untuk menampilkan semua database
        cur.execute("SHOW DATABASES;")
        databases = cur.fetchall()  # Ambil semua hasil query

        # Format hasil ke dalam bentuk list
        database_list = [db[0] for db in databases]

        return jsonify({"status": "success", "databases": database_list})
    except Exception as e:
        # Tangkap dan tampilkan error jika terjadi masalah
        import traceback
        error_details = traceback.format_exc()
        print("Traceback Error:\n", error_details)
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cur.close()


app.register_blueprint(register_bp, url_prefix='/register')
#app.register_blueprint(faceTrain_bp, url_prefix='/faceTrain')
#app.register_blueprint(facePredict_bp, url_prefix='/facePredict')

if __name__ == '__main__':
    app.run(debug=True)
