import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


def generate_password():
    try:
        length = length_var.get()
    except (ValueError, tk.TclError):
        messagebox.showerror("Error", "Enter a valid password length!")
        return

    if length < 8:
        messagebox.showerror("Error", "Password must contain at least 8 characters!")
        return

    character_sets = []

    if upper_var.get():
        character_sets.append(string.ascii_uppercase)

    if lower_var.get():
        character_sets.append(string.ascii_lowercase)

    if number_var.get():
        character_sets.append(string.digits)

    if symbol_var.get():
        character_sets.append("!@#$%^&*()-_=+[]{}?")

    if len(character_sets) < 2:
        messagebox.showerror("Error", "Select at least two character types!")
        return

    if exclude_var.get():
        ambiguous = "0O1l"
        character_sets = [
            ''.join(char for char in group if char not in ambiguous)
            for group in character_sets
        ]

    # Ensure every selected character set still has usable characters.
    character_sets = [group for group in character_sets if group]
    if len(character_sets) < 2:
        messagebox.showerror(
            "Error",
            "Your selected character types do not contain enough usable characters."
        )
        return

    if length < len(character_sets):
        messagebox.showerror(
            "Error",
            "Password length must be at least the number of selected character types."
        )
        return

    all_characters = ''.join(character_sets)

    # Guarantee at least one character from every selected type.
    password = [secrets.choice(group) for group in character_sets]

    # Fill the remaining positions.
    for _ in range(length - len(password)):
        password.append(secrets.choice(all_characters))

    # Securely shuffle the characters.
    secrets.SystemRandom().shuffle(password)
    final_password = ''.join(password)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, final_password)

    # Copy automatically after generation.
    try:
        pyperclip.copy(final_password)
    except pyperclip.PyperclipException:
        messagebox.showwarning(
            "Clipboard",
            "Password generated, but automatic clipboard copying failed."
        )

    # Keep only the five most recent passwords in memory.
    history.insert(0, final_password)
    del history[5:]

    update_history()
    update_strength(length, len(character_sets))


def update_strength(length, types):
    if length >= 16 and types >= 3:
        strength_label.config(text="Strong", fg="green")
    elif length >= 10 and types >= 2:
        strength_label.config(text="Medium", fg="orange")
    else:
        strength_label.config(text="Weak", fg="red")


def copy_password():
    password = password_entry.get()

    if password:
        try:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied successfully!")
        except pyperclip.PyperclipException:
            messagebox.showerror("Clipboard Error", "Could not copy the password.")
    else:
        messagebox.showwarning("Warning", "Generate a password first!")


def update_history():
    history_list.delete(0, tk.END)

    for password in history:
        history_list.insert(tk.END, password)


# Main window
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x650")
root.resizable(False, False)
root.configure(bg="#202030")

# Variables
length_var = tk.IntVar(value=12)
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=False)
exclude_var = tk.BooleanVar(value=False)

history = []

# Heading
title = tk.Label(
    root,
    text="PASSWORD GENERATOR",
    font=("Arial", 20, "bold"),
    bg="#202030",
    fg="white"
)
title.pack(pady=20)

# Password length
tk.Label(
    root,
    text="Password Length",
    font=("Arial", 12),
    bg="#202030",
    fg="white"
).pack()

length_spinbox = tk.Spinbox(
    root,
    from_=8,
    to=64,
    textvariable=length_var,
    width=10,
    font=("Arial", 12)
)
length_spinbox.pack(pady=10)

# Character selection
tk.Label(
    root,
    text="Choose Character Types",
    font=("Arial", 12, "bold"),
    bg="#202030",
    fg="white"
).pack(pady=10)

options_frame = tk.Frame(root, bg="#202030")
options_frame.pack()

tk.Checkbutton(
    options_frame,
    text="Uppercase (A-Z)",
    variable=upper_var,
    bg="#202030",
    fg="white",
    selectcolor="#404060"
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Lowercase (a-z)",
    variable=lower_var,
    bg="#202030",
    fg="white",
    selectcolor="#404060"
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Numbers (0-9)",
    variable=number_var,
    bg="#202030",
    fg="white",
    selectcolor="#404060"
).pack(anchor="w")

tk.Checkbutton(
    options_frame,
    text="Symbols (!@#$)",
    variable=symbol_var,
    bg="#202030",
    fg="white",
    selectcolor="#404060"
).pack(anchor="w")

# Exclude ambiguous characters
tk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, 1, l)",
    variable=exclude_var,
    bg="#202030",
    fg="white",
    selectcolor="#404060"
).pack(pady=12)

# Password display
password_entry = tk.Entry(
    root,
    width=35,
    font=("Arial", 13),
    justify="center"
)
password_entry.pack(pady=15)

# Generate button
generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    bg="#7657E8",
    fg="white",
    font=("Arial", 12, "bold"),
    width=22
)
generate_button.pack(pady=8)

# Copy button
copy_button = tk.Button(
    root,
    text="Copy to Clipboard",
    command=copy_password,
    bg="#298C78",
    fg="white",
    font=("Arial", 11),
    width=22
)
copy_button.pack(pady=8)

# Strength indicator
tk.Label(
    root,
    text="Password Strength:",
    bg="#202030",
    fg="white",
    font=("Arial", 11)
).pack(pady=(12, 3))

strength_label = tk.Label(
    root,
    text="Not Generated",
    bg="#202030",
    fg="white",
    font=("Arial", 12, "bold")
)
strength_label.pack()

# History heading
tk.Label(
    root,
    text="Recent Passwords (Last 5)",
    bg="#202030",
    fg="white",
    font=("Arial", 12, "bold")
).pack(pady=12)

# History list
history_list = tk.Listbox(
    root,
    width=42,
    height=5,
    font=("Arial", 10)
)
history_list.pack(pady=5)

# Start the application
root.mainloop()
