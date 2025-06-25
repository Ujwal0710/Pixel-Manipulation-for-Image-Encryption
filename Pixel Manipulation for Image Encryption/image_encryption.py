import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def load_image(image_path):
    """Loads an image from the given path."""
    try:
        img = Image.open(image_path)
        return img
    except FileNotFoundError:
        messagebox.showerror("Error", f"Image file not found at '{image_path}'")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Could not open image. {e}")
        return None

def save_image(image, output_path):
    """Saves the image to the given path."""
    try:
        image.save(output_path)
        messagebox.showinfo("Success", f"Image saved to '{output_path}'")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save image. {e}")

def encrypt_image(image, key):
    """Encrypts the image using pixel manipulation."""
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            # Simple XOR encryption with the key
            r = (r + key) % 256
            g = (g + key) % 256
            b = (b + key) % 256
            pixels[x, y] = (r, g, b)
    return image

def decrypt_image(image, key):
    """Decrypts the image using pixel manipulation."""
    pixels = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            # Reverse XOR encryption with the key
            r = (r - key) % 256
            g = (g - key) % 256
            b = (b - key) % 256
            pixels[x, y] = (r, g, b)
    return image

def browse_image():
    """Opens a file dialog to select an image."""
    filename = filedialog.askopenfilename(initialdir=".", title="Select an Image",
                                           filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                                                      ("All files", "*.*")))
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, filename)

def encrypt_button_click():
    """Handles the encrypt button click event."""
    image_path = image_path_entry.get()
    key_str = key_entry.get()

    if not image_path:
        messagebox.showerror("Error", "Please select an image.")
        return

    if not key_str:
        messagebox.showerror("Error", "Please enter an encryption key.")
        return

    try:
        key = int(key_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid key. Please enter an integer.")
        return

    img = load_image(image_path)
    if img is None:
        return

    encrypted_image = encrypt_image(img, key)
    output_path = filedialog.asksaveasfilename(initialdir=".", title="Save Encrypted Image",
                                                filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    if output_path:
        save_image(encrypted_image, output_path)

def decrypt_button_click():
    """Handles the decrypt button click event."""
    image_path = image_path_entry.get()
    key_str = key_entry.get()

    if not image_path:
        messagebox.showerror("Error", "Please select an image.")
        return

    if not key_str:
        messagebox.showerror("Error", "Please enter an encryption key.")
        return

    try:
        key = int(key_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid key. Please enter an integer.")
        return

    img = load_image(image_path)
    if img is None:
        return

    decrypted_image = decrypt_image(img, key)
    output_path = filedialog.asksaveasfilename(initialdir=".", title="Save Decrypted Image",
                                                filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    if output_path:
        save_image(decrypted_image, output_path)

# Create the main window
root = tk.Tk()
root.title("Image Encryption Tool")

# Image path label and entry
image_path_label = tk.Label(root, text="Image Path:")
image_path_label.grid(row=0, column=0, padx=10, pady=10)

image_path_entry = tk.Entry(root, width=40)
image_path_entry.grid(row=0, column=1, padx=10, pady=10)

browse_button = tk.Button(root, text="Browse", command=browse_image)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Key label and entry
key_label = tk.Label(root, text="Encryption Key:")
key_label.grid(row=1, column=0, padx=10, pady=10)

key_entry = tk.Entry(root, width=40)
key_entry.grid(row=1, column=1, padx=10, pady=10)

# Encrypt and Decrypt buttons
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_button_click)
encrypt_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_button_click)
decrypt_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Run the main loop
root.mainloop()
