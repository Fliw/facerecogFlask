from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL
import bcrypt

login_bp = Blueprint('login', __name__)
mysql = MySQL()

@login_bp.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([email, password]):
            return jsonify({"status": "error", "message": "Semua Field Diperlukan!"}), 400

        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT id, name, email, password FROM user WHERE email = %s
            """,
            (email,)
        )
        user = cur.fetchone()
        cur.close()

        if not user:
            return jsonify({"status": "error", "message": "Email tidak ditemukan!"}), 404

        user_id, name, email, hashed_password = user

        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return jsonify({"status": "error", "message": "Password salah!"}), 400

        return jsonify({
            "status": "success",
            "message": "Login berhasil!",
            "data": {
                "id": user_id,
                "name": name,
                "email": email
            }
        })

    return jsonify({"status": "error", "message": "Method Not Allowed!"}), 405