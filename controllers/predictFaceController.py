import face_recognition
import pickle

def predict_face(photo_path, encoding_file):
    """
    Membandingkan wajah di foto dengan encoding yang dikenal.
    Mengembalikan nilai confidence.
    """
    try:
        with open(encoding_file, 'rb') as f:
            known_encodings = pickle.load(f)

        test_image = face_recognition.load_image_file(photo_path)
        test_encodings = face_recognition.face_encodings(test_image)

        if not test_encodings:
            raise ValueError("Wajah target pengguna tidak ditemukan dalam foto!")

        test_encoding = test_encodings[0]

        distances = face_recognition.face_distance(known_encodings, test_encoding)

        confidence = 1 - distances.mean()
        return round(confidence, 2)
    except Exception as e:
        raise ValueError(f"Error dalam prediksi: {str(e)}")
