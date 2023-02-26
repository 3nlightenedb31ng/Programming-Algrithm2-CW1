import tkinter as tk
from tkinter import filedialog
import hashlib
import struct
import os


def calculate_hash(file_path):
    with open(file_path, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        return hashlib.sha256(binary_file_data).hexdigest()


def calculate_signature_hash(file_path):
    with open(file_path, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        signature_hash = hashlib.sha256(binary_file_data).digest()
        packed_signature_hash = struct.pack('32s', signature_hash)
        return hashlib.sha256(packed_signature_hash).hexdigest()


def check_image_integrity(file_path):
    calculated_hash = calculate_hash(file_path)
    calculated_signature_hash = calculate_signature_hash(file_path)
    if calculated_hash == calculated_signature_hash:
        return True
    else:
        return False


def select_file():
    file_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("jpeg files", "*.jpg"), ("all files", "*.*")))
    result = check_image_integrity(file_path)
    with open(file_path, 'rb') as binary_file:
        binary_file_data = binary_file.read(10)
        image_header = binary_file_data.hex()
    if result:
        output_label.config(text='Image Name: ' + os.path.basename(file_path) + '\n' + 'Image Size: ' + str(os.path.getsize(file_path)) + ' bytes' + '\n' + 'Image Header: ' + image_header + '\n' + 'Hash: ' + calculate_hash(file_path) + '\n' + 'Signature Hash: ' + calculate_signature_hash(file_path) + '\n' + 'Image integrity is maintained.')
    else:
       output_label.config(text='Image Name: ' + os.path.basename(file_path) + '\n' + 'Image Size: ' + str(os.path.getsize(file_path)) + ' bytes' + '\n' + 'Image Header: ' + image_header + '\n' + 'Hash: ' + calculate_hash(file_path) + '\n' + 'Signature Hash: ' + calculate_signature_hash(file_path) + '\n' + 'Image integrity is NOT maintained.', fg='red')


def exit_program():
    root.quit()


root = tk.Tk()
root.title('Image Integrity Checker')
root.geometry("600x400")

select_file_button = tk.Button(root, text='Select File', command=select_file)
select_file_button.pack()

output_label = tk.Label(root, text='')
output_label.pack()

exit_button = tk.Button(root, text='Exit', command=exit_program)
exit_button.pack(side='bottom')

root.mainloop()
