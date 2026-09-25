# 🔐 PASS-FORGE

A secure and customizable password generator built with **Python, Flask, HTML, CSS, and JavaScript**.
PASS-FORGE allows users to generate strong passwords by customizing password length and character types.


## 🚀 Live Demo
[**PASS-FORGE**](https://pass-forge.onrender.com)


## ✨ Features

- 🔑 Secure password generation using Python
- 📏 Password length from 4–30 characters
- 🔠 Uppercase letters support
- 🔡 Lowercase letters support
- 🔢 Numbers support
- 🔣 Symbols support
- 📊 Password strength indicator
- 📋 One-click copy functionality
- 🌙 Light/Dark mode
- 📈 Password generation statistics
- 📱 Responsive design
- 🔒 Uses Python `secrets` module for secure random generation

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **HTML5**
- **CSS3**
- **JavaScript**
- **JSON**

🔐 Security Note
PASS-FORGE uses Python's secrets module for password generation instead of the standard random module.\
Generated passwords are not stored in password.json. The JSON file only stores basic generation statistics such as password length and strength.

📌 Future Improvements
Password history management
More advanced password strength analysis
User preferences
Database integration
Cloud deployment
Additional security features
👨‍💻 Author

Anmol Sandhu
BCA Student | Frontend Web Developer | Learning Python


## 📂 Project Structure

```text
PASS-FORGE/
│
├── templates/
│   └── index.html
│
├── app.py
├── password.json
├── requirements.txt
├── .gitignore
└── README.md
