import base64
import os
import io
import face_recognition
import pickle
from flask import Flask, Blueprint, request, jsonify
from PIL import Image


faceTrain_bp = Blueprint('faceTrain', __name__)

BASE_DIR = os.path.join(os.getcwd(), 'images', 'faceRecog')
MODEL_DIR = "models"
MODEL_PATH = "models/students.pkl"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file tidak ditemukan!")
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)

def load_or_create_model():
    model_path = os.path.join(MODEL_DIR, "students.pkl")
    if os.path.exists(model_path):
        with open(model_path, "rb") as file:
            model_data = pickle.load(file)
    else:
        model_data = {}
    return model_data, model_path

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

@faceTrain_bp.route('/mass-train', methods=['POST'])
def mass_train():
    if 'images' not in request.files:
        return jsonify({"error": "No images provided"}), 400
    
    images = request.files.getlist('images')
    name = request.form.get('name')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    model_data, model_path = load_or_create_model()

    if name not in model_data:
        model_data[name] = []

    trained_faces = 0

    for image in images:
        try:
            image_data = face_recognition.load_image_file(image)
            face_encodings = face_recognition.face_encodings(image_data)

            if face_encodings:
                model_data[name].append(face_encodings[0])
                trained_faces += 1
        except Exception as e:
            print(f"Error processing image {image.filename}: {e}")

    with open(model_path, "wb") as file:
        pickle.dump(model_data, file)

    return jsonify({
        "message": f"Successfully trained {trained_faces} images for {name}",
        "name": name
    }), 200

@faceTrain_bp.route('/detect-face', methods=['POST'])
def detect_face():
    try:
        # Muat file PKL
        model_data = load_model()

        # Ambil data gambar dari request
        data = request.json
        image_data = data.get("image")

        if not image_data:
            return jsonify({"message": "Gambar tidak ditemukan"}), 400

        # Decode base64 image
        image_data = base64.b64decode(image_data.split(",")[1])
        image = Image.open(io.BytesIO(image_data))
        image_np = face_recognition.load_image_file(io.BytesIO(image_data))

        # Ekstrak encoding dari gambar
        face_encodings = face_recognition.face_encodings(image_np)

        if not face_encodings:
            return jsonify({"message": "Tidak ada wajah yang terdeteksi"}), 400

        # Ambil encoding pertama
        input_encoding = face_encodings[0]

        # Bandingkan dengan data di model
        for name, encodings in model_data.items():
            for encoding in encodings:
                match = face_recognition.compare_faces([encoding], input_encoding, tolerance=0.4)
                if match[0]:
                    distance = face_recognition.face_distance([encoding], input_encoding)[0].item()  # Ubah ke float
                    nim = name.split("_")[0]  # Contoh nama dalam model: "nim_nama"
                    student_name = "_".join(name.split("_")[1:])
                    return jsonify({"name": student_name, "nim": nim, "distance": distance}), 200
        return jsonify({"message": "Mahasiswa tidak ditemukan"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500