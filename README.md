# 📚 Library Management System

A professional desktop application for managing libraries, developed with Python, Tkinter GUI, and SQLite database. This project was created as a **university semester project**.

---

## ✨ Features

### 🔐 Authentication & User Management
- User login and registration
- Dual-role access control system (Regular User / Administrator)
- Role-based access control (RBAC)

### 📖 Book Management
- ➕ Add new books
- ✏️ Edit book information
- 🗑️ Delete books
- 🔍 Advanced search by title
- 📋 Display comprehensive information (title, author, genre, publication year, status)

### 👥 User Management _(Admin Only)_
- ➕ Add new users
- ✏️ Edit user information
- 🗑️ Delete users
- 📊 View list of all users
- 🔐 Assign administrative privileges

---

## 🛠️ Requirements

- **Python** ≥ 3.6
- Standard libraries (pre-installed):
  - `tkinter` - For GUI
  - `sqlite3` - For database management

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/amirh-ganji/library-manager.git
cd library-manager
```

### 2️⃣ Run the Application
```bash
python library.py
```

> **Note:** The database (`library.db`) is automatically created on first run.

---

## 📁 Project Structure

```
library-manager/
│
├── library.py         # Main application file
├── library.db         # SQLite database (auto-generated)
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

---

## 🎯 Usage Guide

### 📝 Login or Register
1. Run the application
2. Enter username and password in the login window
3. For new users, click the "Register" button

### 📚 Working with Books
**Adding a Book:**
- Click the "Add Book" button
- Enter book information (title, author, genre, year, status)
- Click "Add" to save

**Editing a Book:**
- Select the desired book from the list
- Click the "Edit Book" button
- Make necessary changes and save

**Searching for a Book:**
- Click the "Search Book" button
- Enter the title or part of it
- Results are displayed automatically

**Deleting a Book:**
- Select the desired book and click "Delete Book"

### 👤 User Management _(For Administrators)_
- If the user has admin privileges, the user management section is automatically displayed
- You can add, edit, or delete users

---

## 🗄️ Database Structure

### `books` Table 📖
```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT,
    year INTEGER,
    status TEXT
);
```

### `users` Table 👤
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL
);
```

---

## ⚠️ Security Information

> ⚠️ **Important:** This is an **academic/educational project** and should not be used in production environments without proper security improvements.

### Security Recommendations for Production Use:

- 🔐 **Password Encryption:** Use strong algorithms like `bcrypt` or `Argon2`
  ```python
  from bcrypt import hashpw, checkpw
  # Example: hashed = hashpw(password.encode(), bcrypt.gensalt())
  ```

- 🔒 **Database Connection:**
  - Use environment variables to store sensitive information
  - In production, use dedicated database servers (PostgreSQL, MySQL)

- 🛡️ **Input Validation:** Validate all user inputs

- 🔑 **Access Control:** Carefully manage access levels and permissions

---

## 📝 Usage Example

```python
# Running the application
python library.py

# Steps:
# 1. Register a new user
# 2. Log in to the system
# 3. Add, edit, or delete books
# 4. (For admins) Manage other users
```

---

## 🐛 Troubleshooting

**Issue:** "`tkinter` not found" error
- **Solution:** Install `tkinter` using the following command:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk
  
  # macOS
  brew install python-tk@3.9
  
  # Windows
  # tkinter is pre-installed with Python
  ```

**Issue:** Database error
- **Solution:** Delete the `library.db` file and run the program again

---

## 🎓 Academic Project Information

This project was developed as part of a **university semester assignment**. The main learning objectives included:
- GUI development with Python (Tkinter)
- SQLite database design and implementation
- User authentication and access control
- CRUD operations (Create, Read, Update, Delete)

While this project successfully demonstrates fundamental concepts, it is recommended that any production use includes proper security implementations and error handling.

---

## 🤝 Contributing

While this is an academic project, suggestions for improvements are welcome! Please:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is released under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## 📧 Contact & Feedback

- 🐛 For bug reports, open a new [Issue](https://github.com/amirh-ganji/library-manager/issues)
- 💬 For suggestions, use [Discussions](https://github.com/amirh-ganji/library-manager/discussions)

---

**Made with ❤️ by [amirh-ganji](https://github.com/amirh-ganji)**
