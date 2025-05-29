# 🎓 Face Recognition Attendance System

An AI-powered smart attendance system that uses real-time face recognition and liveness detection to automate attendance marking for educational institutes and organizations.

---

## 🚀 Project Overview

This system leverages **Computer Vision** and **Machine Learning** to recognize faces, verify identity using liveness detection, and mark attendance automatically. It also includes a **Flask-based web portal** for students and admins to interact with the system.

---

## 📌 Features

- 🎥 Real-time face detection & recognition
- 🧠 Liveness detection to prevent spoofing
- 📁 Automated attendance marking
- 🌐 Flask web portal for attendance records
- 📸 Student registration via image upload
- ✅ Admin dashboard for managing data

---

## 🛠️ Tech Stack

| Category         | Tools & Libraries                            |
|------------------|----------------------------------------------|
| Language         | Python                                       |
| Computer Vision  | OpenCV, `face_recognition` library           |
| Web Framework    | Flask                                        |
| Frontend         | HTML, CSS, JavaScript                        |
| Database         | CSV/Excel or SQLite (optional)               |
| Others           | NumPy, OS, datetime, etc.                    |

---

## 📂 Project Structure

Face-Recognition-Attendance-System/
│
├── static/ # CSS, JS files
├── templates/ # HTML templates
├── Images/ # Student face images
├── Attendance/ # Attendance records (CSV)
├── app.py # Main Flask backend
├── face_recognition.py # Face detection & recognition logic
├── liveness_detection.py # Anti-spoofing system
├── register.py # Student registration logic
├── README.md # Project documentation
└── requirements.txt # Python dependencies


---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Face-Recognition-Attendance-System.git
   cd Face-Recognition-Attendance-System
