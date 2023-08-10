import os
import openpyxl
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog, messagebox

def lock_pdf(input_path, output_path, password):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

def execute_locking():
    # Ask the user to select a folder
    folder_path = filedialog.askdirectory(title="Select Folder with PDF Files")

    # Ask the user to select the Excel file containing passwords
    excel_path = filedialog.askopenfilename(title="Select Excel File with Passwords")

    # Load passwords from Excel in alphabetic ascending order
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook.active
    passwords = [str(cell.value) for cell in sheet['A'] if cell.value is not None]
    passwords.sort()  # Sort passwords in ascending order

    # Create a new folder for locked files inside the chosen folder
    output_folder = os.path.join(folder_path, "locked_files")
    os.makedirs(output_folder, exist_ok=True)

    # Process PDF files in the selected folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            password = passwords.pop(0) if passwords else ""  # Use the next password or an empty string
            lock_pdf(input_path, output_path, password)
            print(f"Locked: {filename} with Password: {password}")

    print("PDF locking completed.")
    messagebox.showinfo("Process Complete", "PDF locking process is complete.")


root = tk.Tk()
root.title("PDF Locker")

window_width = 200
window_height = 100
root.geometry(f"{window_width}x{window_height}")

label = tk.Label(root, text="PDF Locker By Yusuf Giovanno")
label.pack()

execute_button = tk.Button(root, text="Execute", command=execute_locking)
execute_button.pack()

labelfooter = tk.Label(root, text="PDSI - Deepublish 2023")
labelfooter.pack()

labelfooter = tk.Label(root, text="Created By : Yusuf Giovanno")
labelfooter.pack()

root.mainloop()
