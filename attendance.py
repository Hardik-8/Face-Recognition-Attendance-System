import cv2
import numpy as np
import dlib
import face_recognition
import os
import pandas as pd
import time
from datetime import datetime
import threading
import tkinter as tk
from tkinter import messagebox
from flask import Flask, render_template, request
import webbrowser

# Flask App
app = Flask(__name__)

# Path to shape predictor
PREDICTOR_PATH = r"H:\\AKS app\\shape_predictor_68_face_landmarks.dat"

# Load images and encode faces
path = 'Images'
images = []
names = []
encodeList = []

for root_dir, dirs, files in os.walk(path):
    for filename in files:
        img_path = os.path.join(root_dir, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = cv2.imread(img_path)
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encodings = face_recognition.face_encodings(img_rgb)
                if encodings:
                    encode = encodings[0]
                    images.append(img)
                    folder_name = os.path.basename(root_dir)
                    names.append(folder_name)
                    encodeList.append(encode)

print("✅ Face Encoding Completed!")

# Liveness Detection
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

def calculate_EAR(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    EAR = (A + B) / (2.0 * C)
    return EAR

def detect_blink(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
        right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
        left_EAR = calculate_EAR(left_eye)
        right_EAR = calculate_EAR(right_eye)
        avg_EAR = (left_EAR + right_EAR) / 2.0
        if avg_EAR < 0.25:
            return True
    return False

def mark_attendance(name):
    file_path = r"H:\\AKS app\\Attendance.xlsx"
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        new_data = pd.DataFrame([[name, timestamp]], columns=["Student Name", "Timestamp"])
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = pd.DataFrame([[name, timestamp]], columns=["Student Name", "Timestamp"])
    df.to_excel(file_path, index=False)
    print(f"✅ Attendance marked for {name}")

def recognize_face():
    global take_button
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open camera!")
        messagebox.showerror("Error", "Camera not detected!")
        return
    blink_count = 0
    attendance_marked = False
    while True:
        success, frame = cap.read()
        if not success:
            print("❌ Error: Could not access camera!")
            break
        if detect_blink(frame):
            blink_count += 1
            print(f"👁️ Blink detected: {blink_count}")
        if blink_count >= 2 and not attendance_marked:
            print("✅ Liveness confirmed!")
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(encodeList, face_encoding)
                face_distances = face_recognition.face_distance(encodeList, face_encoding)
                match_index = np.argmin(face_distances) if matches else None
                if match_index is not None and matches[match_index]:
                    name = names[match_index]
                    mark_attendance(name)
                    y1, x2, y2, x1 = [i * 4 for i in face_location]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.imshow('Face Recognition', frame)
                    cv2.waitKey(1000)
                    print("⏳ Turning off the camera after 5 seconds...")
                    time.sleep(5)
                    cap.release()
                    cv2.destroyAllWindows()
                    take_button.config(state=tk.NORMAL)
                    return
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            take_button.config(state=tk.NORMAL)
            return

def start_recognition():
    global take_button
    take_button.config(state=tk.DISABLED)
    threading.Thread(target=recognize_face, daemon=True).start()

@app.route('/')
def index():
    return '''
    <h2>Smart Attendance System</h2>
    <form action="/search" method="post">
        <label>Enter Student Name:</label>
        <input type="text" name="name">
        <input type="submit" value="Search">
    </form>
    <br>
    <a href="/attendance">😊</a>
    '''

@app.route('/attendance', methods=['GET'])
def attendance():
    file_path = r"H:\\AKS app\\Attendance.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return df.to_html(index=False)
    else:
        return "<h3>No attendance records found.</h3>"

@app.route('/search', methods=['POST'])
def search():
    name = request.form.get('name')
    file_path = r"H:\\AKS app\\Attendance.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        filtered_df = df[df["Student Name"].str.lower() == name.lower()]
        if not filtered_df.empty:
            return filtered_df.to_html(index=False)
        else:
            return "<h3>No records found for this name.</h3>"
    else:
        return "<h3>No attendance records found.</h3>"

# Tkinter GUI
root = tk.Tk()
root.title("Smart Attendance System")
root.geometry("500x300")
root.configure(bg="#1fcede")  # Light blue background

frame = tk.Frame(root, bg="#C0C0C0", bd=2, relief="groove")
frame.place(relx=0.5, rely=0.5, anchor="center")

heading = tk.Label(frame, text="Smart Attendance System 👁", font=("Helvetica", 18, "bold"), bg="#C0C0C0", fg="#000000")
heading.pack(pady=20)

take_button = tk.Button(frame, text="📸 Take Attendance", font=("Arial", 14), bg="#4CAF50", fg="white", padx=20, pady=10, command=start_recognition)
take_button.pack(pady=10)

portal_button = tk.Button(frame, text="🌐 Open Attendance Portal", font=("Arial", 14), bg="#2196F3", fg="white", padx=20, pady=10,
                          command=lambda: threading.Thread(target=lambda: webbrowser.open("http://127.0.0.1:5000"), daemon=True).start())
portal_button.pack(pady=10)

# Start Flask server in background thread
def run_flask():
    app.run(debug=False, use_reloader=False)

threading.Thread(target=run_flask, daemon=True).start()

# Start Tkinter mainloop
root.mainloop()
