import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

# Apply dark theme styles
def apply_dark_theme(widget):
    widget.configure(bg="#2b2b2b", fg="#ffffff", highlightbackground="#444444", highlightcolor="#666666")

# Center the window
def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    size = tuple(int(_) for _ in window.geometry().split("+")[0].split("x"))
    x = screen_width // 2 - size[0] // 2
    y = screen_height // 2 - size[1] // 2
    window.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

# Function to load the file
def load_file():
    global lines
    file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()

    tree.delete(*tree.get_children())
    for idx, line in enumerate(lines):
        tree.insert("", "end", iid=idx, values=(line.strip(), "", ""))

# Function to assign a category
def assign_category():
    selected_items = tree.selection()
    category = category_input.get().strip()

    if not selected_items:
        messagebox.showerror("Error", "Please select at least one line.")
        return

    if not category:
        messagebox.showerror("Error", "Please enter a category.")
        return

    for item in selected_items:
        idx = int(item)
        if idx not in categorized_lines:
            categorized_lines[idx] = []
        if category in categorized_lines[idx]:
            messagebox.showinfo("Info", f"The category '{category}' is already assigned to the selected line.")
        else:
            categorized_lines[idx].append(category)
            update_tree_item(idx)

# Function to remove a category
def remove_category(category, idx):
    if idx in categorized_lines and category in categorized_lines[idx]:
        categorized_lines[idx].remove(category)
        if not categorized_lines[idx]:
            del categorized_lines[idx]
        update_tree_item(idx)
    else:
        messagebox.showinfo("Info", f"The category '{category}' is not assigned to the selected line.")

# Function to assign a tooltip
def assign_tooltip():
    selected_items = tree.selection()
    tooltip = tooltip_input.get().strip()

    if not selected_items:
        messagebox.showerror("Error", "Please select at least one line.")
        return

    if not tooltip:
        messagebox.showerror("Error", "Please enter a tooltip.")
        return

    for item in selected_items:
        idx = int(item)
        if idx in tooltips:
            messagebox.showinfo("Info", f"The selected line already has a tooltip: '{tooltips[idx]}'. To update it, remove the current tooltip first.")
        else:
            tooltips[idx] = tooltip
            update_tree_item(idx)

# Function to remove a tooltip
def remove_tooltip(idx):
    if idx in tooltips:
        del tooltips[idx]
        update_tree_item(idx)
    else:
        messagebox.showinfo("Info", "The selected line does not have a tooltip.")

# Function to update a Treeview item
def update_tree_item(idx):
    line_text = lines[idx].strip()
    category_text = ", ".join(categorized_lines.get(idx, []))
    tooltip_text = tooltips.get(idx, "")
    tree.item(idx, values=(line_text, category_text, tooltip_text))

# Function to convert to JSON
def convert_to_json():
    json_lines = []
    for idx, line in enumerate(lines):
        line_content = line.strip()
        if line_content:
            json_entry = {"name": line_content}
            if idx in categorized_lines:
                if len(categorized_lines[idx]) == 1:
                    json_entry["category"] = categorized_lines[idx][0]
                else:
                    json_entry["categories"] = categorized_lines[idx]
            if idx in tooltips:
                json_entry["tooltip"] = tooltips[idx]
            json_lines.append(json_entry)

    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if save_path:
        # Write JSON with tab-indented formatting
        with open(save_path, 'w') as json_file:
            json_file.write("[\n")
            for entry in json_lines:
                json_file.write("\t" + json.dumps(entry) + ",\n")
            # Remove trailing comma from the last entry
            json_file.seek(json_file.tell() - 2, 0)
            json_file.write("\n]\n")
        messagebox.showinfo("Success", "Lines converted to JSON successfully!")

# Create a right-click menu
def show_context_menu(event):
    item = tree.identify_row(event.y)
    if not item:
        return

    idx = int(item)

    context_menu = tk.Menu(root, tearoff=0, bg="#2b2b2b", fg="#ffffff")

    if idx in categorized_lines:
        category_submenu = tk.Menu(context_menu, tearoff=0, bg="#2b2b2b", fg="#ffffff")
        for category in categorized_lines[idx]:
            category_submenu.add_command(label=category, command=lambda c=category: remove_category(c, idx))
        context_menu.add_cascade(label="Remove Category", menu=category_submenu)

    if idx in tooltips:
        context_menu.add_command(label="Remove Tooltip", command=lambda: remove_tooltip(idx))

    context_menu.post(event.x_root, event.y_root)

# Create the GUI window
root = tk.Tk()
root.title("Text to JSON Converter")
root.geometry("1400x800")  # Adjusted width to ensure text fits properly
root.minsize(1400, 800)  # Minimum size
root.configure(bg="#2b2b2b")
center_window(root)

lines = []
categorized_lines = {}
tooltips = {}

# Apply dark theme to Treeview
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#2b2b2b",
                foreground="#ffffff",
                rowheight=25,
                fieldbackground="#2b2b2b")
style.configure("Treeview.Heading",
                background="#444444",
                foreground="#ffffff",
                font=("Arial", 12, "bold"))
style.map("Treeview", background=[("selected", "#666666")], foreground=[("selected", "#ffffff")])

# Create a frame for the treeview
tree_frame = tk.Frame(root, bg="#2b2b2b")
tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tree = ttk.Treeview(tree_frame, columns=("Name", "Category(s)", "Tooltip"), show="headings", selectmode="extended")
tree.heading("Name", text="Name")
tree.heading("Category(s)", text="Category(s)")
tree.heading("Tooltip", text="Tooltip")
tree.column("Name", width=600)
tree.column("Category(s)", width=200)
tree.column("Tooltip", width=200)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.bind("<Button-3>", show_context_menu)  # Bind right-click to show context menu

# Create a frame for controls and place it on the right
controls_frame = tk.Frame(root, bg="#2b2b2b")
controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

instructions = tk.Label(controls_frame, text="Load a file, select lines, and assign attributes.", font=("Arial", 12), bg="#2b2b2b", fg="#ffffff")
instructions.pack(pady=10)

load_button = tk.Button(controls_frame, text="Load File", command=load_file, font=("Arial", 12), width=18, bg="#444444", fg="#ffffff")
load_button.pack(pady=5)

category_label = tk.Label(controls_frame, text="Category:", font=("Arial", 12), bg="#2b2b2b", fg="#ffffff")
category_label.pack(pady=5)

category_input = tk.Entry(controls_frame, font=("Arial", 12), width=25, bg="#333333", fg="#ffffff", insertbackground="#ffffff")
category_input.pack(pady=5)

assign_button = tk.Button(controls_frame, text="Assign", command=assign_category, font=("Arial", 12), width=18, bg="#444444", fg="#ffffff")
assign_button.pack(pady=5)

remove_category_button = tk.Button(controls_frame, text="Remove", command=lambda: remove_category(category_input.get().strip(), int(tree.selection()[0]) if tree.selection() else -1), font=("Arial", 12), width=18, bg="#444444", fg="#ffffff")
remove_category_button.pack(pady=5)

tooltip_label = tk.Label(controls_frame, text="Tooltip:", font=("Arial", 12), bg="#2b2b2b", fg="#ffffff")
tooltip_label.pack(pady=5)

tooltip_input = tk.Entry(controls_frame, font=("Arial", 12), width=25, bg="#333333", fg="#ffffff", insertbackground="#ffffff")
tooltip_input.pack(pady=5)

assign_tooltip_button = tk.Button(controls_frame, text="Assign", command=assign_tooltip, font=("Arial", 12), width=18, bg="#444444", fg="#ffffff")
assign_tooltip_button.pack(pady=5)

remove_tooltip_button = tk.Button(controls_frame, text="Remove", command=lambda: remove_tooltip(int(tree.selection()[0]) if tree.selection() else -1), font=("Arial", 12), width=18, bg="#444444", fg="#ffffff")
remove_tooltip_button.pack(pady=5)

convert_button = tk.Button(controls_frame, text="Convert to JSON", command=convert_to_json, font=("Arial", 12), width=18, bg="#444444", fg="#ffffff")
convert_button.pack(pady=5)

# Run the GUI
root.mainloop()
