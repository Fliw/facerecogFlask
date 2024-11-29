import face_recognition
import os
from PIL import Image

# Path ke folder dataset/photos yang berisi foto mahasiswa
folder_path = 'dataset/foto'  # Ganti dengan path folder foto Anda

def crop_face(image_path):
    # Membaca gambar
    image = face_recognition.load_image_file(image_path)
    
    # Deteksi wajah dalam gambar
    face_locations = face_recognition.face_locations(image)
    
    if len(face_locations) > 0:
        # Ambil wajah pertama yang terdeteksi
        top, right, bottom, left = face_locations[0]
        
        # Crop gambar dengan koordinat wajah yang terdeteksi
        pil_image = Image.open(image_path)
        cropped_image = pil_image.crop((left, top, right, bottom))
        
        return cropped_image
    else:
        print(f"Wajah tidak ditemukan di {image_path}")
        return None

def save_cropped_image(original_image_path, cropped_image):
    # Menyimpan gambar cropped dengan nama yang sama seperti gambar asli
    base_path = original_image_path.rsplit('.', 1)[0]  # Mengambil nama file tanpa ekstensi
    new_image_path = base_path + "_cropped.jpg"
    
    # Pastikan gambar diubah menjadi mode RGB untuk menyimpan dalam format JPEG
    if cropped_image.mode == 'RGBA':
        cropped_image = cropped_image.convert('RGB')
    
    # Simpan gambar cropped
    cropped_image.save(new_image_path, 'JPEG')
    print(f"Foto cropped disimpan di {new_image_path}")
    return new_image_path


# Loop untuk meng-crop setiap foto di folder dataset/photo
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Memastikan file adalah gambar
        file_path = os.path.join(folder_path, filename)
        print(f"Mencoba crop gambar: {filename}")
        
        # Crop dan simpan foto
        cropped_image = crop_face(file_path)
        
        if cropped_image:
            new_image_path = save_cropped_image(file_path, cropped_image)
            os.replace(new_image_path, file_path)  # Ganti gambar lama dengan gambar cropped
            print(f"Foto {filename} berhasil di-crop dan diganti.")
        else:
            print(f"Foto {filename} tidak terdeteksi wajahnya.")
