import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# اتصال به دیتابیس SQLite و ایجاد دیتابیس در صورت عدم وجود
def connect_db():
    return sqlite3.connect("library.db")

# ایجاد جداول در دیتابیس
def create_table(conn):
    with conn as db:
        c = db.cursor()
        # جدول کتاب‌ها
        c.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                year INTEGER,
                status TEXT
            )
        ''')
        # جدول کاربران
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL
            )
        ''')

# فرم ثبت‌نام کاربر جدید
def register_user(conn):
    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()
        is_admin = is_admin_var.get()

        if username and password:
            with conn as db:
                c = db.cursor()
                try:
                    c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
                    db.commit()
                    window.destroy()
                except Exception as e:
                    print(f"Error registering user: {e}")
                    messagebox.showerror("خطا", f"Error registering user: {e}")

    window = tk.Toplevel()
    window.title("ثبت نام")
    window.geometry('230x150')
    window.resizable(False, False)


    ttk.Label(window, text="نام کاربری:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="رمز عبور:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    is_admin_var = tk.IntVar()
    ttk.Checkbutton(window, text="ادمین", variable=is_admin_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Button(window, command=submit_registration).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# فرم ورود کاربر
def login_user(conn):
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()

        with conn as db:
            c = db.cursor()
            c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = c.fetchone()
            if user:
                window.destroy()
                open_main_window(conn, user)
            else:
                messagebox.showerror("خطا", "نام کاربری یا رمز عبور نادرست است")

    window = tk.Tk()
    window.title("ورود")
    window.resizable(False, False)

    ttk.Label(window, text="نام کاربری:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="رمز عبور:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(window, text="ورود", command=submit_login).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    ttk.Button(window, text="ثبت نام", command=lambda: register_user(conn)).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    window.mainloop()

# باز کردن پنجره اصلی برنامه کتابخانه
def open_main_window(conn, user):
    window = tk.Tk()
    window.title("کتابخانه")
    # window.resizable(False, False)

    book_list = ttk.Treeview(window, columns=("id", "title", "author", "genre", "year", "status"), show='headings')
    book_list.heading("id", text="ID")
    book_list.heading("title", text="عنوان")
    book_list.heading("author", text="نویسنده")
    book_list.heading("genre", text="ژانر")
    book_list.heading("year", text="سال")
    book_list.heading("status", text="وضعیت")
    book_list.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
    show_books(conn, book_list)

    ttk.Button(window, text="نمایش کتاب ها", command=lambda: show_books(conn, book_list)).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(window, text="افزودن کتاب", command=lambda: add_book(conn, book_list)).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(window, text="ویرایش کتاب", command=lambda: edit_book(conn, book_list)).grid(row=1, column=2, padx=5, pady=5)
    ttk.Button(window, text="جستجوی کتاب", command=lambda: search_book(conn, book_list)).grid(row=1, column=3, padx=5, pady=5)
    ttk.Button(window, text="حذف کتاب", command=lambda: delete_book(conn, book_list)).grid(row=1, column=4, padx=5, pady=5)

    if user[3]:  # Check if the user is admin
        user_list = ttk.Treeview(window, columns=("id", "username", "password", "is_admin"), show='headings')
        user_list.heading("id", text="ID")
        user_list.heading("username", text="نام کاربری")
        user_list.heading("password", text="رمز عبور")
        user_list.heading("is_admin", text="ادمین")
        user_list.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
        show_users(conn, user_list)

        ttk.Button(window, text="نمایش کاربر ها", command=lambda: show_users(conn, user_list)).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(window, text="افزودن کاربر", command=lambda: add_user(conn, user_list)).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(window, text="ویرایش کاربر", command=lambda: edit_user(conn, user_list)).grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(window, text="حذف کاربر", command=lambda: delete_user(conn, user_list)).grid(row=3, column=3, padx=5, pady=5)

    window.mainloop()

# نمایش لیست کتاب‌ها
def show_books(conn, book_list):
    with conn as db:
        c = db.cursor()
        c.execute('SELECT * FROM books')
        books = c.fetchall()
        book_list.delete(*book_list.get_children())
        for book in books:
            book_list.insert('', 'end', values=book)

# فرم افزودن کتاب جدید
def add_book(conn, book_list):
    def submit_book():
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()
        status = status_entry.get()

        if title and author:
            with conn as db:
                c = db.cursor()
                try:
                    c.execute('INSERT INTO books (title, author, genre, year, status) VALUES (?, ?, ?, ?, ?)', (title, author, genre, year, status))
                    db.commit()
                    show_books(conn, book_list)
                    window.destroy()
                except Exception as e:
                    print(f"Error adding book: {e}")
                    messagebox.showerror("خطا", f"Error adding book: {e}")

    window = tk.Toplevel()
    window.title("افزودن کتاب")
    window.resizable(False, False)

    ttk.Label(window, text="عنوان:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = ttk.Entry(window)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="نویسنده:").grid(row=1, column=0, padx=5, pady=5)
    author_entry = ttk.Entry(window)
    author_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(window, text="ژانر:").grid(row=2, column=0, padx=5, pady=5)
    genre_entry = ttk.Entry(window)
    genre_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(window, text="سال:").grid(row=3, column=0, padx=5, pady=5)
    year_entry = ttk.Entry(window)
    year_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(window, text="وضعیت:").grid(row=4, column=0, padx=5, pady=5)
    status_entry = ttk.Entry(window)
    status_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(window, text="افزودن", command=submit_book).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# فرم ویرایش کتاب
def edit_book(conn, book_list):
    selected_item = book_list.selection()
    if not selected_item:
        messagebox.showerror("خطا", "کتابی انتخاب نشده است")
        return

    book = book_list.item(selected_item)["values"]

    def submit_edit():
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()
        status = status_entry.get()

        if title and author:
            with conn as db:
                c = db.cursor()
                try:
                    c.execute('UPDATE books SET title = ?, author = ?, genre = ?, year = ?, status = ? WHERE id = ?', (title, author, genre, year, status, book[0]))
                    db.commit()
                    show_books(conn, book_list)
                    window.destroy()
                except Exception as e:
                    print(f"Error editing book: {e}")
                    messagebox.showerror("خطا", f"Error editing book: {e}")

    window = tk.Toplevel()
    window.title("ویرایش کتاب")
    window.resizable(False, False)

    ttk.Label(window, text="عنوان:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = ttk.Entry(window)
    title_entry.insert(0, book[1])
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="نویسنده:").grid(row=1, column=0, padx=5, pady=5)
    author_entry = ttk.Entry(window)
    author_entry.insert(0, book[2])
    author_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(window, text="ژانر:").grid(row=2, column=0, padx=5, pady=5)
    genre_entry = ttk.Entry(window)
    genre_entry.insert(0, book[3])
    genre_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(window, text="سال:").grid(row=3, column=0, padx=5, pady=5)
    year_entry = ttk.Entry(window)
    year_entry.insert(0, book[4])
    year_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(window, text="وضعیت:").grid(row=4, column=0, padx=5, pady=5)
    status_entry = ttk.Entry(window)
    status_entry.insert(0, book[5])
    status_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(window, text="ذخیره", command=submit_edit).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# حذف کتاب
def delete_book(conn, book_list):
    selected_item = book_list.selection()
    if not selected_item:
        messagebox.showerror("خطا", "کتابی انتخاب نشده است")
        return

    book = book_list.item(selected_item)["values"]

    with conn as db:
        c = db.cursor()
        try:
            c.execute('DELETE FROM books WHERE id = ?', (book[0],))
            db.commit()
            show_books(conn, book_list)
        except Exception as e:
            print(f"Error deleting book: {e}")
            messagebox.showerror("خطا", f"Error deleting book: {e}")

# جستجوی کتاب
def search_book(conn, book_list):
    def submit_search():
        search_term = search_entry.get()
        with conn as db:
            c = db.cursor()
            c.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + search_term + '%',))
            books = c.fetchall()
            book_list.delete(*book_list.get_children())
            for book in books:
                book_list.insert('', 'end', values=book)
        window.destroy()

    window = tk.Toplevel()
    window.title("جستجوی کتاب")
    window.resizable(False, False)

    ttk.Label(window, text="عنوان:").grid(row=0, column=0, padx=5, pady=5)
    search_entry = ttk.Entry(window)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(window, text="جستجو", command=submit_search).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# نمایش لیست کاربران
def show_users(conn, user_list):
    with conn as db:
        c = db.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        user_list.delete(*user_list.get_children())
        for user in users:
            user_list.insert('', 'end', values=user)

# فرم افزودن کاربر جدید
def add_user(conn, user_list):
    def submit_user():
        username = username_entry.get()
        password = password_entry.get()
        is_admin = is_admin_var.get()

        if username and password:
            with conn as db:
                c = db.cursor()
                try:
                    c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
                    db.commit()
                    show_users(conn, user_list)
                    window.destroy()
                except Exception as e:
                    print(f"Error adding user: {e}")
                    messagebox.showerror("خطا", f"Error adding user: {e}")

    window = tk.Toplevel()
    window.title("افزودن کاربر")
    window.resizable(False, False)

    ttk.Label(window, text="نام کاربری:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="رمز عبور:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    is_admin_var = tk.IntVar()
    ttk.Checkbutton(window, text="ادمین", variable=is_admin_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Button(window, text="افزودن", command=submit_user).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# فرم ویرایش کاربر
def edit_user(conn, user_list):
    selected_item = user_list.selection()
    if not selected_item:
        messagebox.showerror("خطا", "کاربری انتخاب نشده است")
        return

    user = user_list.item(selected_item)["values"]

    def submit_edit():
        username = username_entry.get()
        password = password_entry.get()
        is_admin = is_admin_var.get()

        if username and password:
            with conn as db:
                c = db.cursor()
                try:
                    c.execute('UPDATE users SET username = ?, password = ?, is_admin = ? WHERE id = ?', (username, password, is_admin, user[0]))
                    db.commit()
                    show_users(conn, user_list)
                    window.destroy()
                except Exception as e:
                    print(f"Error editing user: {e}")
                    messagebox.showerror("خطا", f"Error editing user: {e}")

    window = tk.Toplevel()
    window.title("ویرایش کاربر")
    window.resizable(False, False)

    ttk.Label(window, text="نام کاربری:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.insert(0, user[1])
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="رمز عبور:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window)
    password_entry.insert(0, user[2])
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    is_admin_var = tk.IntVar()
    is_admin_var.set(user[3])
    ttk.Checkbutton(window, text="ادمین", variable=is_admin_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Button(window, text="ذخیره", command=submit_edit).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# حذف کاربر
def delete_user(conn, user_list):
    selected_item = user_list.selection()
    if not selected_item:
        messagebox.showerror("خطا", "کاربری انتخاب نشده است")
        return

    user = user_list.item(selected_item)["values"]

    with conn as db:
        c = db.cursor()
        try:
            c.execute('DELETE FROM users WHERE id = ?', (user[0],))
            db.commit()
            show_users(conn, user_list)
        except Exception as e:
            print(f"Error deleting user: {e}")
            messagebox.showerror("خطا", f"Error deleting user: {e}")

# تابع اصلی برنامه
def main():
    conn = connect_db()
    create_table(conn)
    login_user(conn)

if __name__ == "__main__":
    main()
