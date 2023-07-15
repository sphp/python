import tkinter as tk
from tkinter import ttk
import sqlite3

class Database:
    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
    def exec(self, query, params=None):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params or ())
            return cursor
    def rows(self, table, columns=None, condition=None, limit=50):
        query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        if limit:
            query += f" LIMIT {limit}"
        return self.exec(query).fetchall()
    def __del__(self):
        self.conn.close()

def view(window, result, columns):
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    for row in result:
        tree.insert("", "end", values=row)
    tree.pack()

# Example usage
root = tk.Tk()
db = Database("ssn.db")
cols = {'fname': 'First Name', 'lname': 'Last Name', 'ssn': 'SSN'}
result = db.rows("ssninfo", list(cols.keys()))
view(root, result, list(cols.values()))
root.mainloop()
