import tkinter as tk
from tkinter import messagebox
import socket
import re
from cryptography.fernet import Fernet

# ======================
# Functions
# ======================

def scan_ports():
    target = ip_entry.get()
    ports = [21, 22, 80, 443]
    result_text.delete(1.0, tk.END)

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))

        if result == 0:
            result_text.insert(tk.END, f"[+] Port {port} OPEN\n")
        else:
            result_text.insert(tk.END, f"[-] Port {port} CLOSED\n")

        sock.close()

def check_password():
    password = password_entry.get()
    strength = 0

    if len(password) >= 8:
        strength += 1
    if re.search("[a-z]", password):
        strength += 1
    if re.search("[A-Z]", password):
        strength += 1
    if re.search("[0-9]", password):
        strength += 1

    if strength >= 4:
        messagebox.showinfo("Result", "Strong Password 💪")
    elif strength >= 2:
        messagebox.showinfo("Result", "Medium Password ⚠️")
    else:
        messagebox.showinfo("Result", "Weak Password ❌")

def encrypt_file():
    key = Fernet.generate_key()
    cipher = Fernet(key)

    file_name = file_entry.get()

    try:
        with open(file_name, "rb") as file:
            data = file.read()

        encrypted = cipher.encrypt(data)

        with open(file_name + ".enc", "wb") as file:
            file.write(encrypted)

        messagebox.showinfo("Success", f"Encrypted!\nKey: {key.decode()}")
    except:
        messagebox.showerror("Error", "File not found!")

# ======================
# UI
# ======================

root = tk.Tk()
root.title("Cyber Security Toolkit")
root.geometry("500x400")

# IP Scanner
tk.Label(root, text="Target IP").pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

tk.Button(root, text="Scan Ports", command=scan_ports).pack()

result_text = tk.Text(root, height=5)
result_text.pack()

# Password
tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root)
password_entry.pack()

tk.Button(root, text="Check Password", command=check_password).pack()

# File Encryption
tk.Label(root, text="File Name").pack()
file_entry = tk.Entry(root)
file_entry.pack()

tk.Button(root, text="Encrypt File", command=encrypt_file).pack()

root.mainloop()