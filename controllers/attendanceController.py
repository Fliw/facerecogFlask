import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

attendance_bp = Blueprint('attendance', __name__)

BASE_DIR = os.path.join(os.getcwd(), 'images', 'faceRecog')

@attendance_bp.route('/', methods=['POST'])
def attendance():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        geolocation = request.form.get('geolocation')
        type_ = request.form.get('type')
        photo = request.files.get('photo')

        if not all([user_id, geolocation, type_, photo]):
            return jsonify({"status": "error", "message": "Semua field (user_id, geolocation, type, photo) diperlukan!"}), 400

        user_folder = os.path.join(BASE_DIR, user_id)
        encoding_file = os.path.join(user_folder, 'face.pkl')

        if not os.path.exists(encoding_file):
            return jsonify({"status": "error", "message": f"Encoding file untuk user ID {user_id} tidak ditemukan!"}), 404

        try:
            photo_path = os.path.join(user_folder, secure_filename(photo.filename))
            photo.save(photo_path)

            from controllers.predictFaceController import predict_face
            confidence = predict_face(photo_path, encoding_file)
            os.remove(photo_path)

            return jsonify({
                "status": "success",
                "message": "Attendance berhasil diproses!",
                "data": {
                    "user_id": user_id,
                    "geolocation": geolocation,
                    "type": type_,
                    "face_confidence_value": confidence
                }
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "error", "message": "Method Not Allowed!"}), 405
