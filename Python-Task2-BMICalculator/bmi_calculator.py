
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt


# --------------------------------
# 1. DATABASE SETUP
# --------------------------------

def create_database():
    try:
        conn = sqlite3.connect("bmi_records.db")

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT,
                date TEXT
            )
        """)

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        root.destroy()


# --------------------------------
# 2. BMI CALCULATION
# --------------------------------

def calculate_bmi():

    username = name_entry.get().strip()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    # Input validation
    if not username or not weight_text or not height_text:
        messagebox.showerror(
            "Input Error",
            "Please fill in all the fields."
        )
        return

    try:
        weight = float(weight_text)
        height = float(height_text)

        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be greater than zero."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numeric values."
        )
        return

    # Calculate BMI
    bmi = weight / (height * height)
    bmi = round(bmi, 2)

    # Classify BMI
    if bmi < 18.5:
        category = "Underweight"
        color = "orange"

    elif bmi < 25:
        category = "Normal"
        color = "green"

    elif bmi < 30:
        category = "Overweight"
        color = "orange"

    else:
        category = "Obese"
        color = "red"

    # Display result
    result_label.config(
        text=f"Your BMI: {bmi}\nCategory: {category}",
        fg=color
    )

    # Save record in database
    try:
        conn = sqlite3.connect("bmi_records.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bmi_records
            (username, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            username,
            weight,
            height,
            bmi,
            category,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "BMI record saved successfully!"
        )

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not save record: {e}"
        )


# --------------------------------
# 3. VIEW BMI HISTORY
# --------------------------------

def view_history():

    username = name_entry.get().strip()

    if not username:
        messagebox.showerror(
            "Input Error",
            "Please enter a username first."
        )
        return

    try:
        conn = sqlite3.connect("bmi_records.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT weight, height, bmi, category, date
            FROM bmi_records
            WHERE username = ?
            ORDER BY id DESC
        """, (username,))

        records = cursor.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo(
                "History",
                "No records found for this user."
            )
            return

        history = f"BMI HISTORY - {username}\n\n"

        for record in records:
            history += (
                f"Date: {record[4]}\n"
                f"Weight: {record[0]} kg\n"
                f"Height: {record[1]} m\n"
                f"BMI: {record[2]}\n"
                f"Category: {record[3]}\n"
                "--------------------------\n"
            )

        messagebox.showinfo("BMI History", history)

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# --------------------------------
# 4. BMI TREND GRAPH
# --------------------------------

def show_graph():

    username = name_entry.get().strip()

    if not username:
        messagebox.showerror(
            "Input Error",
            "Please enter a username first."
        )
        return

    try:
        conn = sqlite3.connect("bmi_records.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT bmi, date
            FROM bmi_records
            WHERE username = ?
            ORDER BY id ASC
        """, (username,))

        records = cursor.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo(
                "Graph",
                "No BMI records available to display."
            )
            return

        bmi_values = [record[0] for record in records]
        dates = [
            datetime.strptime(
                record[1], "%Y-%m-%d %H:%M:%S"
            ).strftime("%d-%m-%Y %H:%M")
            for record in records
        ]

        plt.figure(figsize=(9, 5))

        plt.plot(
            range(1, len(bmi_values) + 1),
            bmi_values,
            marker="o",
            linewidth=2
        )

        plt.xticks(
            range(1, len(dates) + 1),
            dates,
            rotation=30,
            ha="right"
        )

        plt.xlabel("Date")
        plt.ylabel("BMI Value")
        plt.title(f"BMI Trend for {username}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


# --------------------------------
# 5. GUI DESIGN
# --------------------------------

root = tk.Tk()

root.title("BMI Calculator")
root.geometry("450x550")
root.configure(bg="#f0f4f8")
root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text="BMI CALCULATOR",
    font=("Arial", 22, "bold"),
    bg="#f0f4f8",
    fg="#1a5276"
)

heading.pack(pady=25)


# Input frame
input_frame = tk.Frame(
    root,
    bg="#f0f4f8"
)

input_frame.pack(pady=10)


# Username
tk.Label(
    input_frame,
    text="User Name:",
    font=("Arial", 12),
    bg="#f0f4f8"
).grid(row=0, column=0, padx=10, pady=10, sticky="w")

name_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=20
)

name_entry.grid(row=0, column=1, pady=10)


# Weight
tk.Label(
    input_frame,
    text="Weight (kg):",
    font=("Arial", 12),
    bg="#f0f4f8"
).grid(row=1, column=0, padx=10, pady=10, sticky="w")

weight_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=20
)

weight_entry.grid(row=1, column=1, pady=10)


# Height
tk.Label(
    input_frame,
    text="Height (m):",
    font=("Arial", 12),
    bg="#f0f4f8"
).grid(row=2, column=0, padx=10, pady=10, sticky="w")

height_entry = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=20
)

height_entry.grid(row=2, column=1, pady=10)


# Calculate button
calculate_button = tk.Button(
    root,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    bg="#2874a6",
    fg="white",
    width=20,
    command=calculate_bmi
)

calculate_button.pack(pady=15)


# Result
result_label = tk.Label(
    root,
    text="Enter your details to calculate BMI",
    font=("Arial", 14, "bold"),
    bg="#f0f4f8",
    fg="#333333"
)

result_label.pack(pady=15)


# History button
history_button = tk.Button(
    root,
    text="View BMI History",
    font=("Arial", 11),
    width=20,
    command=view_history
)

history_button.pack(pady=7)


# Graph button
graph_button = tk.Button(
    root,
    text="View BMI Trend Graph",
    font=("Arial", 11),
    width=20,
    command=show_graph
)

graph_button.pack(pady=7)


# --------------------------------
# 6. RUN APPLICATION
# --------------------------------

create_database()

root.mainloop()
