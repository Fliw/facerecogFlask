import os
from flask import Blueprint, render_template, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from datetime import datetime
from bcrypt import hashpw, gensalt

register_bp = Blueprint('register', __name__)
mysql = MySQL()

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'images', 'faceRecog')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@register_bp.route('/', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        front_face = request.files.get('front_face')
        left_face = request.files.get('left_face')
        right_face = request.files.get('right_face')

        if not all([name, email, front_face, left_face, right_face]):
            return jsonify({"status": "error", "message": "Semua Field Diperlukan!"}), 400
        
        password = hashpw(email.encode('utf-8'), gensalt()).decode('utf-8')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                """
                INSERT INTO user (name, email, password, created_at, modified_at) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, email, password, current_time, current_time)
            )
            mysql.connection.commit()
            user_id = cur.lastrowid
            cur.close()
            user_folder = os.path.join(UPLOAD_FOLDER, str(user_id))
            os.makedirs(user_folder, exist_ok=True)

            front_path = os.path.join(user_folder, f"{secure_filename(name)}1.jpg")
            left_path = os.path.join(user_folder, f"{secure_filename(name)}2.jpg")
            right_path = os.path.join(user_folder, f"{secure_filename(name)}3.jpg")

            front_face.save(front_path)
            left_face.save(left_path)
            right_face.save(right_path)

            return jsonify({
                "status": "success",
                "message": "User registered successfully!",
                "data": {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    "front_face": front_path,
                    "left_face": left_path,
                    "right_face": right_path,
                }
            })
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
