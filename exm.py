import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

data_file = "work_hours.csv"


root = tk.Tk()
root.title("Облік робочого часу")


def add_entry():
    try:
        task_name = task_entry.get()
        start_time = start_time_entry.get()
        end_time = end_time_entry.get()

        # Перетворення часів у формат datetime
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        work_duration = (end - start).seconds / 3600 
        
        # Додавання запису до CSV
        new_entry = {
            "Task": task_name,
            "Start Time": start_time,
            "End Time": end_time,
            "Duration": work_duration
        }
        
        if pd.io.common.file_exists(data_file):
            df = pd.read_csv(data_file)
        else:
            df = pd.DataFrame(columns=["Task", "Start Time", "End Time", "Duration"])

        new_entry_df = pd.DataFrame([new_entry])
        df = pd.concat([df, new_entry_df], ignore_index=True) #об`єднюємо старі дані з новою стрічкою
        df.to_csv(data_file, index=False)
        
        messagebox.showinfo("Успіх", f"Запис про {task_name} успішно додано!")
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")

task_label = tk.Label(root, text="Назва завдання:")
task_label.pack()
task_entry = tk.Entry(root)
task_entry.pack()

start_time_label = tk.Label(root, text="Час початку (HH:MM):")
start_time_label.pack()
start_time_entry = tk.Entry(root)
start_time_entry.pack()

end_time_label = tk.Label(root, text="Час завершення (HH:MM):")
end_time_label.pack()
end_time_entry = tk.Entry(root)
end_time_entry.pack()

add_button = tk.Button(root, text="Додати запис", command=add_entry)
add_button.pack()


def generate_report():
    try:
        df = pd.read_csv(data_file)
        total_hours = df["Duration"].sum()
        tasks = df["Task"].unique()

        report = f"Загальна кількість відпрацьованих годин: {total_hours} годин\n\nЗавдання:\n"
        for task in tasks:
            task_duration = df[df["Task"] == task]["Duration"].sum()
            report += f"{task}: {task_duration} годин\n"
        
        messagebox.showinfo("Звіт", report)
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")

report_button = tk.Button(root, text="Генерувати звіт", command=generate_report)
report_button.pack()


def visualize_productivity():
    try:
        df = pd.read_csv(data_file)
        task_durations = df.groupby("Task")["Duration"].sum()

        # Побудова графіку
        task_durations.plot(kind="bar", title="Продуктивність за завданнями")
        plt.xlabel("Завдання")
        plt.ylabel("Відпрацьовані години")
        plt.show()
    except Exception as e:
        messagebox.showerror("Помилка", f"Сталася помилка: {e}")

visualize_button = tk.Button(root, text="Візуалізувати продуктивність", command=visualize_productivity)
visualize_button.pack()
root.mainloop()
