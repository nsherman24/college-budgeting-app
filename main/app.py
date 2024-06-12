import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main.backend import BudgetingBackend

class BudgetingApp:
    def __init__(self, root, backend):
        self.root = root
        self.backend = backend
        self.root.title("Budgeting App")
        self.root.geometry("800x600")

        # Set custom fonts
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.entry_font = tkFont.Font(family="Helvetica", size=12)
        self.button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        self.selected_category = None

        # Create the main layout
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.sidebar_frame = tk.Frame(root, width=200, bg="#e0e0e0")
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.update_sidebar()

        # Add Category Frame
        self.category_frame = tk.LabelFrame(self.main_frame, text="Add/Edit Category", font=self.title_font, bg="#f0f0f0", bd=2)
        self.category_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(self.category_frame, text="Category Name", font=self.label_font, bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.category_name = tk.Entry(self.category_frame, font=self.entry_font)
        self.category_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.category_frame, text="Type", font=self.label_font, bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.category_type = tk.Entry(self.category_frame, font=self.entry_font)
        self.category_type.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.category_frame, text="Limit", font=self.label_font, bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        self.category_limit = tk.Entry(self.category_frame, font=self.entry_font)
        self.category_limit.grid(row=2, column=1, padx=5, pady=5)

        self.add_category_btn = tk.Button(self.category_frame, text="Add Category", font=self.button_font, bg="#4caf50", fg="white", command=self.add_or_edit_category)
        self.add_category_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

        # Add Expense Frame
        expense_frame = tk.LabelFrame(self.main_frame, text="Add Expense", font=self.title_font, bg="#f0f0f0", bd=2)
        expense_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(expense_frame, text="Category", font=self.label_font, bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.category_dropdown = ttk.Combobox(expense_frame, state="readonly", font=self.entry_font)
        self.category_dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(expense_frame, text="Amount", font=self.label_font, bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.expense_amount = tk.Entry(expense_frame, font=self.entry_font)
        self.expense_amount.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(expense_frame, text="Notes", font=self.label_font, bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
        self.expense_notes = tk.Entry(expense_frame, font=self.entry_font)
        self.expense_notes.grid(row=2, column=1, padx=5, pady=5)

        add_expense_btn = tk.Button(expense_frame, text="Add Expense", font=self.button_font, bg="#2196f3", fg="white", command=self.add_expense)
        add_expense_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

        # Save Button
        save_btn = tk.Button(self.main_frame, text="Save", font=self.button_font, bg="#ff9800", fg="white", command=self.save_data)
        save_btn.grid(row=2, column=0, pady=10, padx=5, sticky="ew")

        # Pie Chart Frame
        self.pie_chart_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.pie_chart_frame.grid(row=3, column=0, pady=10, padx=5, sticky="ew")

        self.update_category_dropdown()
        self.create_pie_chart()

    def update_sidebar(self):
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()

        tk.Label(self.sidebar_frame, text="Categories", bg="#e0e0e0", font=self.title_font).pack(pady=10)

        for category in self.backend.get_category_names():
            frame = tk.Frame(self.sidebar_frame, bg="#e0e0e0")
            frame.pack(fill=tk.X, pady=2)

            tk.Label(frame, text=category, bg="#e0e0e0", font=self.label_font).pack(side=tk.LEFT, padx=10)

            edit_btn = tk.Button(frame, text="Edit", font=self.button_font, bg="#ffeb3b", command=lambda c=category: self.edit_category(c))
            edit_btn.pack(side=tk.RIGHT, padx=5)

            delete_btn = tk.Button(frame, text="Delete", font=self.button_font, bg="#f44336", fg="white", command=lambda c=category: self.delete_category(c))
            delete_btn.pack(side=tk.RIGHT, padx=5)

    def edit_category(self, category):
        self.selected_category = category
        category_data = self.backend.get_categories()[category]

        self.category_name.delete(0, tk.END)
        self.category_name.insert(0, category)

        self.category_type.delete(0, tk.END)
        self.category_type.insert(0, category_data['type'])

        self.category_limit.delete(0, tk.END)
        self.category_limit.insert(0, category_data['limit'])

        self.add_category_btn.config(text="Update Category")

    def delete_category(self, category):
        success, message = self.backend.delete_category(category)
        messagebox.showinfo("Result", message)
        if success:
            self.update_sidebar()
            self.update_category_dropdown()
            self.create_pie_chart()

    def add_or_edit_category(self):
        name = self.category_name.get()
        category_type = self.category_type.get()
        limit = self.category_limit.get()

        if not name or not category_type or not limit:
            messagebox.showwarning("Input Error", "All fields must be filled.")
            return

        try:
            limit = float(limit)
        except ValueError:
            messagebox.showwarning("Input Error", "Limit must be a number.")
            return

        if self.selected_category:
            success, message = self.backend.update_category(self.selected_category, name, category_type, limit)
        else:
            success, message = self.backend.add_category(name, category_type, limit)

        messagebox.showinfo("Result", message)
        if success:
            self.reset_category_fields()
            self.update_sidebar()
            self.update_category_dropdown()
            self.create_pie_chart()

    def reset_category_fields(self):
        self.selected_category = None
        self.add_category_btn.config(text="Add Category")
        self.category_name.delete(0, tk.END)
        self.category_type.delete(0, tk.END)
        self.category_limit.delete(0, tk.END)

    def update_category_dropdown(self):
        self.category_dropdown['values'] = self.backend.get_category_names()

    def add_expense(self):
        category = self.category_dropdown.get()
        amount = self.expense_amount.get()
        notes = self.expense_notes.get()

        if not category or not amount:
            messagebox.showwarning("Input Error", "Category and Amount must be filled.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a number.")
            return

        success, message = self.backend.add_expense(category, amount, notes)
        if success:
            self.create_pie_chart()
            self.expense_amount.delete(0, tk.END)
            self.expense_notes.delete(0, tk.END)
        messagebox.showinfo("Result", message)

    def create_pie_chart(self):
        for widget in self.pie_chart_frame.winfo_children():
            widget.destroy()

        labels, sizes = self.backend.get_pie_chart_data()

        if not sizes:
            return

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax.axis('equal')

        pie_chart = FigureCanvasTkAgg(fig, master=self.pie_chart_frame)
        pie_chart.get_tk_widget().pack()
        pie_chart.draw()

    def save_data(self):
        message = self.backend.save_data()
        messagebox.showinfo("Result", message)

if __name__ == "__main__":
    root = tk.Tk()
    backend = BudgetingBackend()
    app = BudgetingApp(root, backend)
    root.mainloop()
