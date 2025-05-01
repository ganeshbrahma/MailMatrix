<p align="center">
  <img src="static/mailmatrix-logo.png" width="300" alt="MailMatrix Logo">
</p>

# 📬 MailMatrix

MailMatrix is a cloud-native serverless web application to automate bulk email notifications using AWS services like Lambda, SES, S3, EventBridge, and CloudWatch. It features a Flask frontend for user registration, login, and file uploads.

---

## 🌟 Features
- Register/Login System (Flask + SQLite)
- Upload recipient CSVs and offer letter PDFs
- Send conditional offer/rejection emails using SES
- Uses AWS Lambda + EventBridge for automation
- Tracks upload and email history per user

---

## 💻 Tech Stack

| Frontend | Backend | Cloud | DB |
|----------|---------|--------|----|
| HTML/CSS | Python, Flask | AWS (Lambda, SES, S3, EventBridge, Aurora and RDS, IAM, CloudWatch)

---

## 📁 Project Structure
MailMatrix/ ├── app.py ├── controllers/ ├── static/ │ ├── css/ │ └── images/ ├── templates/ │ ├── login.html │ ├── register.html │ ├── home.html │ ├── profile.html │ └── history.html ├── lambda/ │ └── email_handler.py ├── assets/ │ └── logo.png └── README.md
