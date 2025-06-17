import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def select_file():
    filetypes = (
        ("CSV files", "*.csv"),
        ("All files", "*.*")
    )

    file = fd.askopenfiles(
        title="Select a file",
        initialdir="./",
        filetypes=filetypes
    )

    showinfo(
        title="Selected File",
        message=f"You selected: {file[0].name if file else 'No file selected'}"
    )

def create_window():
    window = tk.Tk()
    window.title("Benfords Law Detector")

    window.geometry("400x300")
    window.configure(bg="lightblue")
    label = tk.Label(window, text="Benford's Law Detector", bg="lightblue", font=("Times New Roman", 12))
    file_button = tk.Button(window, text="Select CSV File", command=select_file, bg="white", font=("Arial", 10))
    
    label.pack(pady=20)
    file_button.pack(pady=20)

    

    window.mainloop()






if __name__ == "__main__":
    create_window()