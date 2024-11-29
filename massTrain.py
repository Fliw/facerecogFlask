import os
import pandas as pd
import requests

URL = "http://localhost:5000/faceTrain/mass-train"

# Lokasi file Excel dan folder foto
EXCEL_PATH = "dataset/mhs.xlsx"
PHOTO_DIR = "dataset/foto"

# Membaca file Excel
def read_excel_data(excel_path):
    df = pd.read_excel(excel_path)
    # Pastikan field NIM dan Nama sesuai dengan header di Excel Anda
    if "NIM" not in df.columns or "Nama" not in df.columns:
        raise ValueError("File Excel harus memiliki kolom 'NIM' dan 'Nama'")
    return df

# Mendapatkan path foto berdasarkan NIM
def get_photo_path(nim):
    # Mengubah format NIM ke format nama file (xx_xx_xxxx.jpg)
    photo_filename = nim.replace(".", "_") + ".jpg"
    photo_path = os.path.join(PHOTO_DIR, photo_filename)
    return photo_path if os.path.exists(photo_path) else None

# Mengirim data ke Flask endpoint
def send_training_data(excel_path, url):
    df = read_excel_data(excel_path)
    for _, row in df.iterrows():
        nim = row["NIM"]
        name = row["Nama"]
        photo_path = get_photo_path(nim)
        
        if not photo_path:
            print(f"Foto untuk NIM {nim} tidak ditemukan. Lewati.")
            continue
        
        try:
            # Kirim data dengan requests
            with open(photo_path, "rb") as photo_file:
                response = requests.post(
                    url,
                    data={"name": name},
                    files={"images": photo_file}
                )
            if response.status_code == 200:
                #add response time for training
                print(f"===============================")
                print(f"face encoding training success for NIM {nim} ({name}).")
                print(f"Training Response time: {response.elapsed.total_seconds()} seconds")
                print(f"===============================\n")
            else:
                print(f"Gagal mengirim data untuk NIM {nim} ({name}): {response.text}")
        except Exception as e:
            print(f"Error saat mengirim data untuk NIM {nim} ({name}): {e}")

# Main script
if __name__ == "__main__":
    try:
        send_training_data(EXCEL_PATH, URL)
    except Exception as e:
        print(f"Error: {e}")
