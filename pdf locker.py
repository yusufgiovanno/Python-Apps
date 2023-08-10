import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import PyPDF2

output_folder = "locked_pdfs"

def lock_pdf(input_path, output_path, password):
    with open(input_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        pdf_writer.encrypt(password)

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def exec_lock():
    input_folder = folderinput
    password = password_entry.get()

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_subfolder = os.path.join(input_folder, output_folder)  # New subfolder path
            os.makedirs(output_subfolder, exist_ok=True)  # Create subfolder if not exists
            output_path = os.path.join(output_subfolder, filename)
            lock_pdf(input_path, output_path, password)
            print(f"Locked: {filename}")

    messagebox.showinfo("Information", "Done.")

def browse_folder():
    global folderinput
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_label.config(text=folder_path)
        folderinput = folder_path
        submit_button.pack()  # Show the submit button when folder is picked

def password_changed(*args):
    if folderinput and password_entry.get():
        submit_button.pack()  # Show the submit button when both folder and password are filled
    else:
        submit_button.pack_forget()  # Hide the submit button

root = tk.Tk()
root.title("PDF Locker By Yusuf Giovanno")

folderinput = ""

label = tk.Label(root, text="Select a Folder:")
label.pack()

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack()

folder_path_label = tk.Label(root, text="Folder File PDF:")
folder_path_label.pack()

password_label = tk.Label(root, text="Enter Password:")
password_label.pack()

password_var = tk.StringVar()
password_var.trace_add("write", password_changed)  # Call password_changed when password is written

password_entry = tk.Entry(root, textvariable=password_var)
password_entry.pack()

submit_button = tk.Button(root, text="Lock PDF(s)", command=exec_lock)

root.mainloop()