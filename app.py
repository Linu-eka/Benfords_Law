import tkinter as tk
from tkinter import filedialog as fd
from process_file import ProcessFile
from benfords import calculate_benfords

def select_file(filename_label, result_text):
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
        total_items, comparison_result = calculate_benfords(amounts)
        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)

        formatted = ""
        # Format the comparison_result dictionary for display
        for digit, data in comparison_result.items():
            formatted += f"Digit: {digit} Expected: {data['expected']:.2f}% Real: {data['real']:.2f}% Difference: {data['difference']:.2f}%\n"

        result_text.insert(tk.END, formatted)
        result_text.config(state='disabled')


    else:
        filename_label.config(text="No file selected")

def create_window():
    window = tk.Tk()
    window.title("Benfords Law Detector")

    window.geometry("800x400")
    window.configure(bg="lightblue")
    label = tk.Label(window, text="Benford's Law Detector", bg="lightblue", font=("Times New Roman", 12))
    file_button = tk.Button(window, text="Select CSV File", bg="white", font=("Times New Roman", 10))
    filename_label = tk.Label(window, text="No file selected", bg="lightblue", font=("Times New Roman", 10))
    result_label = tk.Label(window, text="Results:", bg="lightblue", font=("Times New Roman", 12))
    result_text = tk.Text(window, height=10, width=80, bg="white", font=("Times New Roman", 10), state='disabled')
    file_button.config(command=lambda: select_file(filename_label,result_text))
    
    label.pack(pady=20)
    file_button.pack(pady=20)
    
    filename_label.pack()
    result_label.pack(pady=10,padx=10,anchor='w')
    result_text.pack(pady=10,padx=10, anchor='w')


    

    window.mainloop()






if __name__ == "__main__":
    create_window()