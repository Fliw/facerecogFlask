import os
import face_recognition
import pickle
from flask import Blueprint, request, jsonify

faceTrain_bp = Blueprint('faceTrain', __name__)

BASE_DIR = os.path.join(os.getcwd(), 'images', 'faceRecog')

@faceTrain_bp.route('/train', methods=['POST'])
def train():
    if request.method == 'POST':
        user_id = request.form.get('user_id')

        if not user_id:
            return jsonify({"status": "error", "message": "Field user_id diperlukan!"}), 400
        
        user_folder = os.path.join(BASE_DIR, user_id)
        
        if not os.path.exists(user_folder):
            return jsonify({"status": "error", "message": f"Folder untuk user ID {user_id} tidak ditemukan!"}), 404
        
        image_files = [
            os.path.join(user_folder, file)
            for file in os.listdir(user_folder)
            if file.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
        
        if not image_files:
            return jsonify({"status": "error", "message": "Tidak ada file gambar untuk training!"}), 400

        try:
            encodings = []
            
            for image_file in image_files:
                image = face_recognition.load_image_file(image_file)
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    encodings.append(face_encodings[0])
                else:
                    return jsonify({"status": "error", "message": f"Tidak ditemukan wajah di file: {os.path.basename(image_file)}"}), 400
            
            encoding_file = os.path.join(user_folder, 'face.pkl')
            with open(encoding_file, 'wb') as f:
                pickle.dump(encodings, f)
            
            return jsonify({
                "status": "success",
                "message": "Berhasil training dan encode face!",
                "data": {
                    "user_id": user_id,
                    "encoding_file": encoding_file
                }
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "error", "message": "Method Not Allowed!"}), 405
