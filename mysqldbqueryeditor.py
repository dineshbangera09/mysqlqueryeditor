import os
import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # If python-dotenv is not installed, fall back to environment variables
    pass

# Database connection
def connect_db(database=None):
    kwargs = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'kiosk'),
        'password': os.getenv('DB_PASSWORD', 'Vision#123'),
    }
    port = os.getenv('DB_PORT')
    if port:
        try:
            kwargs['port'] = int(port)
        except ValueError:
            pass
    if database:
        kwargs['database'] = database
    return mysql.connector.connect(**kwargs)

# Function to list all databases
def list_databases():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SHOW DATABASES')
    databases = [row[0] for row in cursor.fetchall()]
    conn.close()
    return databases

# Function to execute an arbitrary query and return results or affected rows
def execute_query(query, database=None):
    conn = connect_db(database)
    cursor = conn.cursor()
    cursor.execute(query)
    result = None
    columns = None
    rowcount = None
    if cursor.with_rows:
        result = cursor.fetchall()
        columns = cursor.column_names
    else:
        conn.commit()
        rowcount = cursor.rowcount
    conn.close()
    return columns, result, rowcount


# Function to get health status (e.g., database connectivity)
def get_health_status():
    try:
        conn = connect_db(database=self.selected_database)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return "Healthy"
    except Exception as e:
        return f"Unhealthy ({str(e)})"

# GUI for dashboard
class KioskDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Query Editor - MySQL Database Dashboard")
        self.root.geometry("1200x820")

        self.selected_database = None

        # Health Status Label
        self.health_label = ttk.Label(root, text="Health Status: Checking...", font=("Arial", 12, "bold"))
        self.health_label.pack(pady=10)

        self.update_button = ttk.Button(root, text="Refresh Data", command=self.update_data)
        self.update_button.pack(pady=10)

        # Query panel
        query_frame = ttk.LabelFrame(root, text="Database Query Editor", padding=10)
        query_frame.pack(padx=10, pady=5, fill="both", expand=True)

        left_panel = ttk.Frame(query_frame)
        left_panel.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(left_panel, text="Databases:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.db_listbox = tk.Listbox(left_panel, height=14, width=28)
        self.db_listbox.pack(fill="y", expand=True)
        self.db_listbox.bind("<<ListboxSelect>>", self.on_database_select)

        self.db_refresh_button = ttk.Button(left_panel, text="Reload Databases", command=self.load_databases)
        self.db_refresh_button.pack(pady=6, fill="x")

        self.db_label = ttk.Label(left_panel, text="Selected DB: kiosk", font=("Arial", 9))
        self.db_label.pack(anchor="w", pady=(6, 0))

        right_panel = ttk.Frame(query_frame)
        right_panel.pack(side="left", fill="both", expand=True)

        ttk.Label(right_panel, text="Enter SQL query:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.query_text = tk.Text(right_panel, height=8, wrap="none")
        self.query_text.pack(fill="both", expand=False)

        query_button_frame = ttk.Frame(right_panel)
        query_button_frame.pack(fill="x", pady=6)

        self.run_query_button = ttk.Button(query_button_frame, text="Run Query", command=self.run_query)
        self.run_query_button.pack(side="left")

        self.query_status_label = ttk.Label(query_button_frame, text="Ready", font=("Arial", 9))
        self.query_status_label.pack(side="left", padx=10)

        output_frame = ttk.LabelFrame(right_panel, text="Query Output", padding=5)
        output_frame.pack(fill="both", expand=True)

        self.output_tree = ttk.Treeview(output_frame, show="headings")
        self.output_tree.pack(side="left", fill="both", expand=True)

        output_scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_tree.yview)
        self.output_tree.configure(yscroll=output_scrollbar.set)
        output_scrollbar.pack(side="right", fill="y")

        self.output_message_label = ttk.Label(output_frame, text="", font=("Arial", 9))
        self.output_message_label.pack(anchor="w", pady=(4, 0))

        self.load_databases()
        self.update_data()

    def load_databases(self):
        try:
            databases = list_databases()
            self.db_listbox.delete(0, tk.END)
            for db in databases:
                self.db_listbox.insert(tk.END, db)
            self.query_status_label.config(text="Databases loaded")
        except Exception as e:
            self.query_status_label.config(text=f"Database list error: {e}")
            self.output_message_label.config(text="")

    def on_database_select(self, event):
        selected = self.db_listbox.curselection()
        if selected:
            self.selected_database = self.db_listbox.get(selected[0])
            self.db_label.config(text=f"Selected DB: {self.selected_database}")
        else:
            self.selected_database = None
            self.db_label.config(text="Selected DB: kiosk")

    def run_query(self):
        query = self.query_text.get(1.0, tk.END).strip()
        if not query:
            self.query_status_label.config(text="Enter a SQL query first")
            return

        database = self.selected_database or 'kiosk'
        try:
            columns, rows, rowcount = execute_query(query, database=database)
            self.render_query_output(columns, rows, rowcount)
            self.query_status_label.config(text="Query executed successfully")
        except Exception as e:
            self.output_tree.delete(*self.output_tree.get_children())
            self.output_tree['columns'] = ()
            self.output_tree['show'] = ''
            self.output_message_label.config(text=f"Error: {e}")
            self.query_status_label.config(text="Query failed")

    def render_query_output(self, columns, rows, rowcount):
        self.output_tree.delete(*self.output_tree.get_children())
        if columns:
            self.output_tree['columns'] = columns
            self.output_tree['show'] = 'headings'
            for col in columns:
                self.output_tree.heading(col, text=col)
                self.output_tree.column(col, width=140, anchor='w')
            for row in rows:
                self.output_tree.insert('', 'end', values=row)
            self.output_message_label.config(text=f"Returned {len(rows)} rows")
        else:
            self.output_tree['columns'] = ()
            self.output_tree['show'] = ''
            self.output_message_label.config(text=f"Query OK, {rowcount} rows affected")

    def update_data(self):
        # Update health status
        health = get_health_status()
        self.health_label.config(text=f"Health Status: {health}")


if __name__ == "__main__":
    root = tk.Tk()
    app = KioskDashboard(root)
    root.mainloop()