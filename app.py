import tkinter as tk
from tkinter import filedialog as fd
from process_file import ProcessFile

def select_file(filename_label):
    filetypes = (
        ("CSV files", "*.csv"),
    )

    file = fd.askopenfiles(
        title="Select a file",
        initialdir="./",
        filetypes=filetypes
    )

    if file:
        filename_label.config(text=f"Selected: {file[0].name}")
        amounts = ProcessFile(file[0].name)
        print("Amounts extracted:", amounts)  # For debugging purposes

    else:
        filename_label.config(text="No file selected")

def create_window():
    window = tk.Tk()
    window.title("Benfords Law Detector")

    window.geometry("800x300")
    window.configure(bg="lightblue")
    label = tk.Label(window, text="Benford's Law Detector", bg="lightblue", font=("Times New Roman", 12))
    file_button = tk.Button(window, text="Select CSV File", bg="white", font=("Times New Roman", 10))
    filename_label = tk.Label(window, text="No file selected", bg="lightblue", font=("Times New Roman", 10))
    
    file_button.config(command=lambda: select_file(filename_label))
    
    label.pack(pady=20)
    file_button.pack(pady=20)
    
    filename_label.pack()

    

    window.mainloop()






if __name__ == "__main__":
    create_window()