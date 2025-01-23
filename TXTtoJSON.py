import json
import tkinter as tk
from tkinter import filedialog, messagebox

def text_to_json(input_file, output_file):
    # Initialize an empty list to store the lines
    data = []
    
    # Read the text file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Read each line, replace fancy apostrophes, and add to the list
            for line in f:
                clean_line = line.replace("’", "'")  # Replace fancy apostrophe
                data.append({"name": f"{clean_line.strip()}"})
        
        # Write to JSON file with desired formatting
        with open(output_file, 'w') as f:
            f.write("[\n")  # Start the JSON array
            for i, item in enumerate(data):
                # Write each object on its own line without escaping non-ASCII characters
                f.write(f'\t{json.dumps(item, ensure_ascii=False)}')
                # Add a comma unless it's the last item
                if i < len(data) - 1:
                    f.write(",\n")
                else:
                    f.write("\n")
            f.write("]\n")  # Close the JSON array
        
        messagebox.showinfo("Success", f"Successfully converted {input_file} to {output_file}")
            
    except FileNotFoundError:
        messagebox.showerror("Error", f"Could not find file {input_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



def browse_input_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, filename)

def convert():
    input_file = input_entry.get()
    output_file = output_entry.get()
    if input_file and output_file:
        text_to_json(input_file, output_file)
    else:
        messagebox.showwarning("Warning", "Please select both input and output files")

if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    root.title("Text to JSON Converter")
    root.geometry("500x200")
    
    # Input file selection
    tk.Label(root, text="Input Text File:").pack(pady=5)
    input_frame = tk.Frame(root)
    input_frame.pack(fill=tk.X, padx=20)
    input_entry = tk.Entry(input_frame)
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(input_frame, text="Browse", command=browse_input_file).pack(side=tk.RIGHT, padx=5)
    
    # Output file selection
    tk.Label(root, text="Output JSON File:").pack(pady=5)
    output_frame = tk.Frame(root)
    output_frame.pack(fill=tk.X, padx=20)
    output_entry = tk.Entry(output_frame)
    output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    tk.Button(output_frame, text="Browse", command=browse_output_file).pack(side=tk.RIGHT, padx=5)
    
    # Convert button
    tk.Button(root, text="Convert", command=convert, width=20).pack(pady=20)
    
    root.mainloop()
