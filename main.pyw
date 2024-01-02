# Import Modules
import os
import qrcode
import sys
import tkinter as tk
import tkinter.ttk as ttk
import darkdetect
from PIL import ImageTk, Image
from tkinter import filedialog

# Dark theme title bar imported from https://github.com/alijafari79/Tkinter_dark_Title_bar
import ctypes as ct


def dark_title_bar(window):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    dwmwa_use_immersive_dark_mode = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = dwmwa_use_immersive_dark_mode
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


# Detect dark mode
if darkdetect.isDark():
    dark = True
else:
    dark = False

# Dark mode variables
bg_color = "#202020"
button_bg_color = "#333333"
fg_color = "#FFFFFF"
font = ("Segoe UI", 9)
highlight_button = "#454545"

# Create the main Tkinter window
root = tk.Tk()
root.minsize(width=318, height=368)
root.title("QR Coder")

# Set window icon
icon = tk.PhotoImage(file="assets/icon.png")
root.iconphoto(True, icon)

# Configure window grid
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create a LabelFrame for organizing widgets
if dark:
    label_frame = tk.LabelFrame(root, text="QR Coder", fg=fg_color, font=font, bd=1)
    label_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
else:
    label_frame = ttk.LabelFrame(root, text="QR Coder")
    label_frame.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")

# Configure LabelFrame grid
label_frame.rowconfigure(0, weight=1)
label_frame.rowconfigure(1, weight=0)
label_frame.rowconfigure(2, weight=0)
label_frame.columnconfigure(0, weight=1)
label_frame.columnconfigure(1, weight=1)

# Creating "image_path" variable
image_path = "assets/qrcode.png"

# Entry widget for input
if dark:
    entry = tk.Entry(label_frame, width=25, background=button_bg_color, fg=fg_color, bd=1)
    entry.grid(row=1, column=0, padx=5, pady=7, sticky="SEW")
else:
    entry = ttk.Entry(label_frame, width=25)
    entry.grid(row=1, column=0, padx=5, pady=7, sticky="SEW")

# Create "qr" variable
qr = None


# Function to handle button click and generate QR code


def generate_button_command():
    img = qrcode.make(entry.get())
    img.save(image_path)
    global qr
    qr = ImageTk.PhotoImage(Image.open(image_path))
    qr_code_display_label.configure(image=qr)
    qr_code_save_button.configure(state="normal")


# Button to trigger QR code generation
if dark:
    generate_button = tk.Button(label_frame, text="Generate", command=generate_button_command,
                                background=button_bg_color, fg=fg_color, font=font, bd=0,
                                activebackground=highlight_button, activeforeground=fg_color)
    generate_button.grid(row=1, column=1, padx=5, pady=5, sticky="SEW")
else:
    generate_button = ttk.Button(label_frame, text="Generate", command=generate_button_command)
    generate_button.grid(row=1, column=1, padx=5, pady=5, sticky="SEW")

# Display the initial QR code image
qr_code_display_label = tk.Label(label_frame)
qr_code_display_label.grid(row=0, column=0, sticky="NSEW", columnspan=2, padx=5, pady=5)


# Function to handle button click and save QR code image


def save_qr_code():
    f = tk.filedialog.asksaveasfile(initialfile="qrcode.png", filetypes=[("PNG - Portable Network Graphics", ".png")])
    try:
        (Image.open(image_path)).save(f.name)
    except AttributeError:
        pass


# Button to save QR code image
if dark:
    qr_code_save_button = tk.Button(label_frame, text="Save", command=save_qr_code, state="disabled",
                                    background=button_bg_color, fg=fg_color, font=font, bd=0,
                                    activebackground=highlight_button, activeforeground=fg_color)
    qr_code_save_button.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5, columnspan=2, ipady=10)
else:
    qr_code_save_button = ttk.Button(label_frame, text="Save", command=save_qr_code, state="disabled")
    qr_code_save_button.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5, columnspan=2, ipady=10)

# Setting dark theme
if dark:
    root.configure(background=bg_color)
    label_frame.configure(background=bg_color, foreground=fg_color)
    qr_code_display_label.configure(background=bg_color)
    dark_title_bar(root)
root.configure(width=root.winfo_width()+1)

# Start the Tkinter event loop
root.mainloop()

# Remove generated file
try:
    os.remove(image_path)
    sys.exit()
except FileNotFoundError:
    sys.exit()
