import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connecting to the SQLite database and creating the database if it does not exist
def connect_db():
    return sqlite3.connect("library.db")

# Creating tables in the database
def create_table(conn):
    with conn as db:
        c = db.cursor()
        # Table of books
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
        # Users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL
            )
        ''')

# New user registration form
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
                    messagebox.showerror("Error", f"Error registering user: {e}")

    window = tk.Toplevel()
    window.title("Register")
    window.geometry('230x150')
    window.resizable(False, False)


    ttk.Label(window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    is_admin_var = tk.IntVar()
    ttk.Checkbutton(window, text="Admin", variable=is_admin_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Button(window, command=submit_registration).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# User login form
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
                messagebox.showerror("Error", "The username or password is incorrect.")

    window = tk.Tk()
    window.title("Login")
    window.resizable(False, False)

    ttk.Label(window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(window, text="Login", command=submit_login).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    ttk.Button(window, text="Register", command=lambda: register_user(conn)).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    window.mainloop()

# Open the main window of the Library application.
def open_main_window(conn, user):
    window = tk.Tk()
    window.title("کتابخانه")
    # window.resizable(False, False)

    book_list = ttk.Treeview(window, columns=("id", "title", "author", "genre", "year", "status"), show='headings')
    book_list.heading("id", text="ID")
    book_list.heading("title", text="Title")
    book_list.heading("author", text="Author")
    book_list.heading("genre", text="Genre")
    book_list.heading("year", text="Year")
    book_list.heading("status", text="Status")
    book_list.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
    show_books(conn, book_list)

    ttk.Button(window, text="Show books", command=lambda: show_books(conn, book_list)).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(window, text="Add a book", command=lambda: add_book(conn, book_list)).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(window, text="Book editing", command=lambda: edit_book(conn, book_list)).grid(row=1, column=2, padx=5, pady=5)
    ttk.Button(window, text="Book search", command=lambda: search_book(conn, book_list)).grid(row=1, column=3, padx=5, pady=5)
    ttk.Button(window, text="Delete book", command=lambda: delete_book(conn, book_list)).grid(row=1, column=4, padx=5, pady=5)

    if user[3]:  # Check if the user is admin
        user_list = ttk.Treeview(window, columns=("id", "username", "password", "is_admin"), show='headings')
        user_list.heading("id", text="ID")
        user_list.heading("username", text="Username")
        user_list.heading("password", text="Password")
        user_list.heading("is_admin", text="Admin")
        user_list.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
        show_users(conn, user_list)

        ttk.Button(window, text="Show users", command=lambda: show_users(conn, user_list)).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(window, text="Add user", command=lambda: add_user(conn, user_list)).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(window, text="Edit user", command=lambda: edit_user(conn, user_list)).grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(window, text="Delete user", command=lambda: delete_user(conn, user_list)).grid(row=3, column=3, padx=5, pady=5)

    window.mainloop()

# Show list of books
def show_books(conn, book_list):
    with conn as db:
        c = db.cursor()
        c.execute('SELECT * FROM books')
        books = c.fetchall()
        book_list.delete(*book_list.get_children())
        for book in books:
            book_list.insert('', 'end', values=book)

# Add new book form
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
                    messagebox.showerror("Error", f"Error adding book: {e}")

    window = tk.Toplevel()
    window.title("Add a book")
    window.resizable(False, False)

    ttk.Label(window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = ttk.Entry(window)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="Author:").grid(row=1, column=0, padx=5, pady=5)
    author_entry = ttk.Entry(window)
    author_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(window, text="Genre:").grid(row=2, column=0, padx=5, pady=5)
    genre_entry = ttk.Entry(window)
    genre_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(window, text="Year:").grid(row=3, column=0, padx=5, pady=5)
    year_entry = ttk.Entry(window)
    year_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(window, text="Status:").grid(row=4, column=0, padx=5, pady=5)
    status_entry = ttk.Entry(window)
    status_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(window, text="Add", command=submit_book).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Book editing form
def edit_book(conn, book_list):
    selected_item = book_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "No book selected.")
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
                    messagebox.showerror("Error", f"Error editing book: {e}")

    window = tk.Toplevel()
    window.title("Book editing")
    window.resizable(False, False)

    ttk.Label(window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = ttk.Entry(window)
    title_entry.insert(0, book[1])
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="Author:").grid(row=1, column=0, padx=5, pady=5)
    author_entry = ttk.Entry(window)
    author_entry.insert(0, book[2])
    author_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(window, text="Genre:").grid(row=2, column=0, padx=5, pady=5)
    genre_entry = ttk.Entry(window)
    genre_entry.insert(0, book[3])
    genre_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(window, text="Year:").grid(row=3, column=0, padx=5, pady=5)
    year_entry = ttk.Entry(window)
    year_entry.insert(0, book[4])
    year_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(window, text="Status:").grid(row=4, column=0, padx=5, pady=5)
    status_entry = ttk.Entry(window)
    status_entry.insert(0, book[5])
    status_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(window, text="Save", command=submit_edit).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Delete book
def delete_book(conn, book_list):
    selected_item = book_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "No book selected.")
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
            messagebox.showerror("Error", f"Error deleting book: {e}")

# Book search
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
    window.title("Book search")
    window.resizable(False, False)

    ttk.Label(window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    search_entry = ttk.Entry(window)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(window, text="Search", command=submit_search).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Show user list
def show_users(conn, user_list):
    with conn as db:
        c = db.cursor()
        c.execute('SELECT * FROM users')
        users = c.fetchall()
        user_list.delete(*user_list.get_children())
        for user in users:
            user_list.insert('', 'end', values=user)

# Add new user form
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
                    messagebox.showerror("Error", f"Error adding user: {e}")

    window = tk.Toplevel()
    window.title("Add user")
    window.resizable(False, False)

    ttk.Label(window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window)
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    is_admin_var = tk.IntVar()
    ttk.Checkbutton(window, text="Admin", variable=is_admin_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Button(window, text="Add", command=submit_user).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# User edit form
def edit_user(conn, user_list):
    selected_item = user_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "No user selected.")
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
                    messagebox.showerror("Error", f"Error editing user: {e}")

    window = tk.Toplevel()
    window.title("Edit user")
    window.resizable(False, False)

    ttk.Label(window, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(window)
    username_entry.insert(0, user[1])
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(window, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(window)
    password_entry.insert(0, user[2])
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    is_admin_var = tk.IntVar()
    is_admin_var.set(user[3])
    ttk.Checkbutton(window, text="Admin", variable=is_admin_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    ttk.Button(window, text="Save", command=submit_edit).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Delete user
def delete_user(conn, user_list):
    selected_item = user_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "No user selected.")
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
            messagebox.showerror("Error", f"Error deleting user: {e}")

# Main function of the program
def main():
    conn = connect_db()
    create_table(conn)
    login_user(conn)

if __name__ == "__main__":
    main()
