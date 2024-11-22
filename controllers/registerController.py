from flask import Blueprint, render_template, request, jsonify
from flask_mysqldb import MySQL

register_bp = Blueprint('register', __name__)
mysql = MySQL()

@register_bp.route('/', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            mysql.connection.commit()
            cur.close()
            return jsonify({"status": "success", "message": "User registered successfully!"})
        except Exception as e:
            mysql.connection.rollback()
            return jsonify({"status": "error", "message": str(e)})
    return render_template('register.html')
