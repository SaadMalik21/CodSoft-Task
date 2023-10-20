import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import date, datetime
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

conn = sqlite3.connect('task_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        task_id INTEGER PRIMARY KEY,
        task_name TEXT,
        start_date DATE,
        end_date DATE,
        assigned_person TEXT,
        project_name TEXT,
        completed INTEGER
    )
''')
conn.commit()

root = tk.Tk()
root.title("Task Manager")
root.geometry("800x600")  


def refresh_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    for i in task_table.get_children():
        task_table.delete(i)

    for task in tasks:
        completed = "No"
        if task[5] == 1:
            completed = "Yes"
        task_table.insert("", "end", values=(task[0], task[1], task[2], task[3], task[4], task[5], completed))


background_image = Image.open(r"C:\Users\user\Pictures\PIL\background5.jpg")  
background_image = background_image.resize((800, 600))
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


dashboard_frame = ttk.Frame(root)
dashboard_frame.grid(row=0, column=0, sticky='nsew')


table_frame = ttk.Frame(root)
table_frame.grid(row=1, column=0, sticky='nsew')

notebook = ttk.Notebook(dashboard_frame)
notebook.pack(fill='both', expand=True)

new_task_tab = ttk.Frame(notebook)
notebook.add(new_task_tab, text="Add New Task")

task_name_label = tk.Label(new_task_tab, text="Task Name:")
task_name_label.grid(row=0, column=0)
task_name_entry = tk.Entry(new_task_tab)
task_name_entry.grid(row=0, column=1)

start_date_label = tk.Label(new_task_tab, text="Start Date (YYYY-MM-DD):")
start_date_label.grid(row=1, column=0)
start_date_entry = tk.Entry(new_task_tab)
start_date_entry.grid(row=1, column=1)

end_date_label = tk.Label(new_task_tab, text="End Date (YYYY-MM-DD):")
end_date_label.grid(row=2, column=0)
end_date_entry = tk.Entry(new_task_tab)
end_date_entry.grid(row=2, column=1)

assigned_person_label = tk.Label(new_task_tab, text="Assigned Person:")
assigned_person_label.grid(row=3, column=0)
assigned_person_entry = tk.Entry(new_task_tab)
assigned_person_entry.grid(row=3, column=1)

project_name_label = tk.Label(new_task_tab, text="Project Name:")
project_name_label.grid(row=4, column=0)
project_name_var = tk.StringVar()
project_name_entry = tk.Entry(new_task_tab, textvariable=project_name_var)
project_name_entry.grid(row=4, column=1)

def add_task():
    task_name = task_name_entry.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    assigned_person = assigned_person_entry.get()
    project_name = project_name_var.get()

    if not task_name or not start_date or not end_date or not assigned_person or not project_name:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    cursor.execute('''
        INSERT INTO tasks (task_name, start_date, end_date, assigned_person, project_name, completed)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (task_name, start_date, end_date, assigned_person, project_name, 0))
    conn.commit()

    task_name_entry.delete(0, 'end')
    start_date_entry.delete(0, 'end')
    end_date_entry.delete(0, 'end')
    assigned_person_entry.delete(0, 'end')
    project_name_var.set("")

    refresh_tasks()

add_task_button = tk.Button(new_task_tab, text="Add Task", command=add_task)
add_task_button.grid(row=5, column=0, columnspan=2)

view_tasks_tab = ttk.Frame(notebook)
notebook.add(view_tasks_tab, text="View Tasks")

task_table = ttk.Treeview(view_tasks_tab, columns=("Task ID", "Task Name", "Start Date", "End Date", "Assigned Person", "Project Name", "Completed"))
task_table.heading("#1", text="Task ID")
task_table.heading("#2", text="Task Name")
task_table.heading("#3", text="Start Date")
task_table.heading("#4", text="End Date")
task_table.heading("#5", text="Assigned Person")
task_table.heading("#6", text="Project Name")
task_table.heading("#7", text="Completed")
task_table.grid(row=0, column=0)

def delete_task():
    selected_item = task_table.selection()
    if selected_item:
        task_id = task_table.item(selected_item, 'values')[0]
        cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
        conn.commit()
        refresh_tasks()

delete_button = tk.Button(view_tasks_tab, text="Delete Task", command=delete_task)
delete_button.grid(row=1, column=0)

def mark_as_completed():
    selected_item = task_table.selection()
    if selected_item:
        task_id = task_table.item(selected_item, 'values')[0]
        cursor.execute("UPDATE tasks SET completed = 1 WHERE task_id = ?", (task_id,))
        conn.commit()
        refresh_tasks()

mark_completed_button = tk.Button(view_tasks_tab, text="Mark as Completed", command=mark_as_completed)
mark_completed_button.grid(row=2, column=0)

update_task_tab = ttk.Frame(notebook)
notebook.add(update_task_tab, text="Update Task")

def fetch_task_details():
    selected_item = task_table.selection()
    if selected_item:
        task_id = task_table.item(selected_item, 'values')[0]
        cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
        task = cursor.fetchone()
        if task:
            
            task_name_entry_update.delete(0, 'end')
            task_name_entry_update.insert(0, task[1])

            start_date_entry_update.delete(0, 'end')
            start_date_entry_update.insert(0, task[2])

            end_date_entry_update.delete(0, 'end')
            end_date_entry_update.insert(0, task[3])

            assigned_person_entry_update.delete(0, 'end')
            assigned_person_entry_update.insert(0, task[4])

            project_name_var_update.set(task[5])


task_name_label_update = tk.Label(update_task_tab, text="Task Name:")
task_name_label_update.grid(row=0, column=0)
task_name_entry_update = tk.Entry(update_task_tab)
task_name_entry_update.grid(row=0, column=1)

start_date_label_update = tk.Label(update_task_tab, text="Start Date (YYYY-MM-DD):")
start_date_label_update.grid(row=1, column=0)
start_date_entry_update = tk.Entry(update_task_tab)
start_date_entry_update.grid(row=1, column=1)

end_date_label_update = tk.Label(update_task_tab, text="End Date (YYYY-MM-DD):")
end_date_label_update.grid(row=2, column=0)
end_date_entry_update = tk.Entry(update_task_tab)
end_date_entry_update.grid(row=2, column=1)

assigned_person_label_update = tk.Label(update_task_tab, text="Assigned Person:")
assigned_person_label_update.grid(row=3, column=0)
assigned_person_entry_update = tk.Entry(update_task_tab)
assigned_person_entry_update.grid(row=3, column=1)

project_name_label_update = tk.Label(update_task_tab, text="Project Name:")
project_name_label_update.grid(row=4, column=0)
project_name_var_update = tk.StringVar()
project_name_entry_update = tk.Entry(update_task_tab, textvariable=project_name_var_update)
project_name_entry_update.grid(row=4, column=1)

def update_task():
    selected_item = task_table.selection()
    if selected_item:
        task_id = task_table.item(selected_item, 'values')[0]
        task_name = task_name_entry_update.get()
        start_date = start_date_entry_update.get()
        end_date = end_date_entry_update.get()
        assigned_person = assigned_person_entry_update.get()
        project_name = project_name_var_update.get()

        if not task_name or not start_date or not end_date or not assigned_person or not project_name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        cursor.execute('''
            UPDATE tasks
            SET task_name = ?, start_date = ?, end_date = ?, assigned_person = ?, project_name = ?
            WHERE task_id = ?
        ''', (task_name, start_date, end_date, assigned_person, project_name, task_id))
        conn.commit()

       
        task_name_entry_update.delete(0, 'end')
        start_date_entry_update.delete(0, 'end')
        end_date_entry_update.delete(0, 'end')
        assigned_person_entry_update.delete(0, 'end')
        project_name_var_update.set("")

        refresh_tasks()

update_button = tk.Button(update_task_tab, text="Update Task", command=update_task)
update_button.grid(row=5, column=0, columnspan=2)


fetch_details_button = tk.Button(update_task_tab, text="Fetch Task Details", command=fetch_task_details)
fetch_details_button.grid(row=6, column=0, columnspan=2)


project_progress_tab = ttk.Frame(notebook)
notebook.add(project_progress_tab, text="Project Progress")


def calculate_project_progress_with_graph():
    project_name = project_name_var_progress.get()
    user_date_str = user_date_entry.get()

    try:
        user_date = datetime.strptime(user_date_str, "%Y-%m-%d").date()
        today = date.today()

       
        cursor.execute("SELECT MIN(start_date), MAX(end_date) FROM tasks WHERE project_name = ?", (project_name,))
        project_dates = cursor.fetchone()

        project_start_date = datetime.strptime(project_dates[0], "%Y-%m-%d").date()
        project_end_date = datetime.strptime(project_dates[1], "%Y-%m-%d").date()

        
        days_worked = (user_date - project_start_date).days

       
        remaining_days = (project_end_date - user_date).days

        if remaining_days > 0:
            progress = (days_worked / (days_worked + remaining_days)) * 100
        else:
            progress = 100

        project_progress_label.config(text=f"Project Progress: {progress:.2f}%")

        
        plt.figure(figsize=(6, 4))
        plt.bar(["Days Worked", "Remaining Days"], [days_worked, remaining_days], color=['blue', 'red'])
        plt.xlabel("Time")
        plt.ylabel("Days")
        plt.title("Project Progress")
        plt.show()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")


project_name_label_progress = tk.Label(project_progress_tab, text="Project Name:")
project_name_label_progress.grid(row=0, column=0)
project_name_var_progress = tk.StringVar()
project_name_entry_progress = tk.Entry(project_progress_tab, textvariable=project_name_var_progress)
project_name_entry_progress.grid(row=0, column=1)


user_date_label = tk.Label(project_progress_tab, text="Today's Date (YYYY-MM-DD):")
user_date_label.grid(row=1, column=0)
user_date_entry = tk.Entry(project_progress_tab)
user_date_entry.grid(row=1, column=1)


calculate_progress_button = tk.Button(project_progress_tab, text="Calculate Progress", command=calculate_project_progress_with_graph)
calculate_progress_button.grid(row=2, column=0, columnspan=2)


project_progress_label = tk.Label(project_progress_tab, text="")
project_progress_label.grid(row=3, column=0, columnspan=2)


def go_to_starting_page():
    notebook.select(0)  


start_page_button = tk.Button(project_progress_tab, text="Begin the Task", command=go_to_starting_page)
start_page_button.grid(row=4, column=0, columnspan=2)

refresh_tasks()

root.mainloop()
