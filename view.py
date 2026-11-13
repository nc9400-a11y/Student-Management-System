"""VIEW - the Tkinter user interface (event-driven programming).

Widgets used (from Unit 5): Tk, Frame, Label, Entry, Button, Menu/Menubutton,
messagebox, plus ttk.Treeview for the table.
Geometry managers used: grid() for the form, pack() for the layout.
The View contains NO database code - it only reports events to the Controller.
"""
import tkinter as tk
from tkinter import ttk, messagebox

# ---- colour palette ----
NAVY = "#1F3A5F"
LIGHT = "#F4F7FB"
ACCENT = "#2E86DE"
GREEN = "#27AE60"
ORANGE = "#F39C12"
RED = "#E74C3C"
GREY = "#7F8C8D"


class StudentView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System  |  MVC + MySQL")
        self.geometry("760x600")
        self.minsize(700, 560)
        self.configure(bg=LIGHT)
        self.controller = None

        self.name_var = tk.StringVar()
        self.reg_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self._build_menu()
        self._build_header()
        self._build_form()
        self._build_table()
        self._build_statusbar()

    # ---------------- layout ----------------
    def _build_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Clear form", command=lambda: self.controller.on_clear())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
            "About", "Student Management System\nPython Tkinter + MySQL\nMVC architecture"))
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _build_header(self):
        header = tk.Frame(self, bg=NAVY, height=70)
        header.pack(fill="x")
        tk.Label(header, text="Student Management System", bg=NAVY, fg="white",
                 font=("Segoe UI", 20, "bold")).pack(pady=(10, 0))
        tk.Label(header, text="Store and view student name and registration number",
                 bg=NAVY, fg="#BFD0E6", font=("Segoe UI", 10)).pack(pady=(0, 8))

    def _build_form(self):
        card = tk.LabelFrame(self, text="  Student Details  ", bg="white", fg=NAVY,
                             font=("Segoe UI", 11, "bold"), padx=15, pady=12)
        card.pack(fill="x", padx=20, pady=(15, 8))

        tk.Label(card, text="Student Name", bg="white", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="w", pady=6)
        self.name_entry = tk.Entry(card, textvariable=self.name_var, width=38,
                                   font=("Segoe UI", 11), relief="solid", bd=1)
        self.name_entry.grid(row=0, column=1, padx=12, pady=6)

        tk.Label(card, text="Registration No.", bg="white", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="w", pady=6)
        self.reg_entry = tk.Entry(card, textvariable=self.reg_var, width=38,
                                  font=("Segoe UI", 11), relief="solid", bd=1)
        self.reg_entry.grid(row=1, column=1, padx=12, pady=6)

        btns = tk.Frame(card, bg="white")
        btns.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        self._button(btns, "Add", GREEN, lambda: self.controller.on_add())
        self._button(btns, "Update", ORANGE, lambda: self.controller.on_update())
        self._button(btns, "Delete", RED, lambda: self.controller.on_delete())
        self._button(btns, "Clear", GREY, lambda: self.controller.on_clear())

    def _button(self, parent, text, colour, command):
        b = tk.Button(parent, text=text, command=command, bg=colour, fg="white",
                      activebackground=NAVY, activeforeground="white",
                      font=("Segoe UI", 10, "bold"), width=11, relief="flat", cursor="hand2")
        b.pack(side="left", padx=6)
        return b

    def _build_table(self):
        top = tk.Frame(self, bg=LIGHT)
        top.pack(fill="x", padx=20, pady=(6, 2))
        tk.Label(top, text="Search:", bg=LIGHT, font=("Segoe UI", 10)).pack(side="left")
        self.search_entry = tk.Entry(top, textvariable=self.search_var, width=30,
                                     font=("Segoe UI", 10), relief="solid", bd=1)
        self.search_entry.pack(side="left", padx=8)
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.on_search())  # event binding
        self.count_label = tk.Label(top, text="Total: 0", bg=LIGHT, fg=NAVY,
                                    font=("Segoe UI", 10, "bold"))
        self.count_label.pack(side="right")

        frame = tk.Frame(self, bg=LIGHT)
        frame.pack(fill="both", expand=True, padx=20, pady=(2, 8))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background=NAVY, foreground="white")
        style.map("Treeview", background=[("selected", ACCENT)])

        self.table = ttk.Treeview(frame, columns=("id", "name", "reg"), show="headings",
                                  selectmode="browse")
        self.table.heading("id", text="ID")
        self.table.heading("name", text="Student Name")
        self.table.heading("reg", text="Registration Number")
        self.table.column("id", width=50, anchor="center")
        self.table.column("name", width=340)
        self.table.column("reg", width=200, anchor="center")
        self.table.tag_configure("odd", background="#EAF1FB")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.table.bind("<<TreeviewSelect>>", self._on_select)   # event: row clicked

    def _build_statusbar(self):
        self.status = tk.Label(self, text="Ready", anchor="w", bg=NAVY, fg="white",
                               font=("Segoe UI", 9), padx=10)
        self.status.pack(fill="x", side="bottom")

    # ---------------- events inside the view ----------------
    def _on_select(self, event=None):
        sel = self.table.selection()
        if sel:
            _, name, reg = self.table.item(sel[0], "values")
            self.name_var.set(name)
            self.reg_var.set(reg)

    # ---------------- methods the Controller calls ----------------
    def bind_controller(self, controller):
        self.controller = controller

    def get_form(self):
        return self.name_var.get(), self.reg_var.get()

    def clear_form(self):
        self.name_var.set("")
        self.reg_var.set("")
        for item in self.table.selection():
            self.table.selection_remove(item)
        self.name_entry.focus_set()

    def get_search(self):
        return self.search_var.get()

    def set_search(self, text):
        self.search_var.set(text)

    def selected_id(self):
        sel = self.table.selection()
        return int(self.table.item(sel[0], "values")[0]) if sel else None

    def show_students(self, students):
        self.table.delete(*self.table.get_children())
        for i, s in enumerate(students):
            self.table.insert("", "end", values=(s.id, s.name, s.reg_no),
                              tags=("odd",) if i % 2 else ())

    def set_count(self, n):
        self.count_label.config(text=f"Total: {n}")

    def set_status(self, text):
        self.status.config(text=text)

    def show_error(self, msg):
        messagebox.showerror("Error", msg)

    def confirm(self, msg):
        return messagebox.askyesno("Confirm", msg)
