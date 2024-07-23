import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

class AnnotationTool:
    def __init__(self, master):
        self.master = master
        master.title("Resume Annotation Tool")

        self.text = tk.Text(master, height=20, width=80)
        self.text.pack()

        self.entity_var = tk.StringVar(master)
        self.entity_var.set("PERSON")  # default value
        self.entity_options = ["PERSON", "EMAIL", "PHONE", "ADDRESS", "JOB_TITLE", "ORGANIZATION", "SKILL"]
        self.entity_menu = tk.OptionMenu(master, self.entity_var, *self.entity_options)
        self.entity_menu.pack()

        self.annotate_button = tk.Button(master, text="Annotate Selection", command=self.annotate_selection)
        self.annotate_button.pack()

        self.save_button = tk.Button(master, text="Save Annotations", command=self.save_annotations)
        self.save_button.pack()

        self.load_button = tk.Button(master, text="Load Resume", command=self.load_resume)
        self.load_button.pack()

        self.annotations = []

    def annotate_selection(self):
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")
            entity_type = self.entity_var.get()
            self.annotations.append([start, end, entity_type])
            self.text.tag_add(entity_type, start, end)
            self.text.tag_config(entity_type, background="yellow")
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select text to annotate")

    def save_annotations(self):
        full_text = self.text.get("1.0", tk.END)
        data = {
            "text": full_text,
            "entities": [[int(self.text.index(start).split('.')[1]), 
                          int(self.text.index(end).split('.')[1]), 
                          entity_type] for start, end, entity_type in self.annotations]
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json")
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

    def load_resume(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as f:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f.read())

if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotationTool(root)
    root.mainloop()