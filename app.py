import tkinter as tk
from tkinter import filedialog as fd
from process_file import ProcessFile
from benfords import calculate_benfords
from scipy.stats import chisquare
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def mean_absolute_deviation(observed, expected):
    observed_prop = np.array(observed) / sum(observed)
    expected_prop = np.array(expected) / sum(expected)
    return np.mean(np.abs(observed_prop - expected_prop))

def select_file(filename_label, result_text, graph_frame):
    filetypes = (
        ("CSV files", "*.csv"),
    )

    file = fd.askopenfiles(
        title="Select a file",
        initialdir="./",
        filetypes=filetypes
    )

    # Remove any previous graph if it exists
    for widget in graph_frame.winfo_children():
        widget.destroy()

    if file:
        '''
        This is where we handle file selection, file processing, and displaying results.
        '''        
        filename_label.config(text=f"Selected: {file[0].name}")
        amounts = ProcessFile(file[0].name)

        # Handle the case where the file could not be processed or does not contain valid data
        if amounts is None:
            result_text.config(state='normal')
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Error processing file. Please ensure it contains valid numeric data.")
            result_text.config(state='disabled')
            return
        
        # Calculate Benford's Law comparison
        _,actual_count,expected_count, comparison_result = calculate_benfords(amounts)
        result_text.config(state='normal')
        result_text.delete(1.0, tk.END)

        # Use chi squared test to compare expected and real distributions
        actual_count_list = [0] * 9
        for digit in range(1, 10):
            actual_count_list[digit - 1] = actual_count.get(str(digit), 0)
        
        actual_count = actual_count_list
        expected_count = list(expected_count.values())
        

        deviation = mean_absolute_deviation(actual_count, expected_count)
        formatted = ""

        # Format the comparison_result dictionary for display
        for digit, data in comparison_result.items():
            formatted += f"Digit: {digit}\t Expected: {data['expected']:.2f}% Real: {data['real']:.2f}% Difference: {data['difference']:.2f}\n"

        # Check if Benford's Law is satisfied based on the deviation
        if deviation < 0.006:
            formatted += "\n Benford's Law is satisfied.\n"
        elif deviation > 0.006 and deviation < 0.012:
            formatted += "\n Benford's Law is moderately satisfied.\n"
        elif deviation > 0.012:
            formatted += "\n Benford's Law is NOT satisfied.\n"
        else:
            formatted += "\n Unable to determine if Benford's Law is satisfied.\n"
        

        result_text.insert(tk.END, formatted)
        result_text.config(state='disabled')

        #Plotting the results on the graph
        fig = Figure(figsize=(10, 5), dpi=100)
        ax = fig.add_subplot(111)
        digits = np.arange(1, 10)
        ax.bar(digits - 0.2, actual_count, width=0.4, label='Actual', color='blue', alpha=0.7)
        ax.bar(digits + 0.2, expected_count, width=0.4, label='Expected', color='orange', alpha=0.7)
        ax.set_xlabel('First Digit')
        ax.set_ylabel('Frequency')
        ax.set_title("Benford's Law Comparison")
        ax.set_xticks(digits)
        ax.set_xticklabels(digits)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        

    else:
        filename_label.config(text="No file selected")

def create_window():
    window = tk.Tk()
    window.title("Benfords Law Detector")
    window.geometry("800x750")
    window.configure(bg="lightblue")

    # Configure grid weights for responsiveness
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=2)
    window.grid_rowconfigure(0, weight=0)
    window.grid_rowconfigure(1, weight=0)
    window.grid_rowconfigure(2, weight=0)
    window.grid_rowconfigure(3, weight=2)
    window.grid_rowconfigure(4, weight=2)

    label = tk.Label(window, text="Benford's Law Detector", bg="lightblue", font=("Times New Roman", 14))
    file_button = tk.Button(window, text="Select CSV File", bg="white", font=("Times New Roman", 10))
    filename_label = tk.Label(window, text="No file selected", bg="lightblue", font=("Times New Roman", 10))
    result_label = tk.Label(window, text="Results:", bg="lightblue", font=("Times New Roman", 12))
    result_text = tk.Text(window, height=15, width=80, bg="white", font=("Times New Roman", 10), state='disabled')

    # Create a graphical representation of the results
    graph_frame = tk.Frame(window, bg="lightblue")
    graph_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    
    file_button.config(command=lambda: select_file(filename_label, result_text, graph_frame))

    # Place widgets using grid
    label.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")
    file_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    filename_label.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")
    result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


    window.mainloop()






if __name__ == "__main__":
    create_window()