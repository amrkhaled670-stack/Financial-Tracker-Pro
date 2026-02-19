
import customtkinter as ctk
from tkinter import ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام إدارة المصاريف الاحترافي")
        self.root.geometry("1100x700")
        
        # تنسيق الألوان
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # قاعدة البيانات
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             category TEXT, amount REAL, date TEXT)''')
        self.conn.commit()

        self.create_ui()
        self.load_data()

    def create_ui(self):
        # القائمة الجانبية (Sidebar)
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="التحكم المالي", font=("Arial", 20, "bold"))
        self.logo.pack(pady=20, padx=10)

        # منطقة المحتوى الرئيسي
        self.main_content = ctk.CTkFrame(self.root)
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # كروت الإدخال
        input_card = ctk.CTkFrame(self.main_content)
        input_card.pack(fill="x", pady=10)

        self.category_entry = ctk.CTkEntry(input_card, placeholder_text="الفئة", width=200)
        self.category_entry.pack(side="right", padx=10, pady=20)

        self.amount_entry = ctk.CTkEntry(input_card, placeholder_text="المبلغ", width=150)
        self.amount_entry.pack(side="right", padx=10, pady=20)

        self.add_btn = ctk.CTkButton(input_card, text="إضافة مصروف", command=self.add_expense)
        self.add_btn.pack(side="right", padx=10, pady=20)

        # الجدول (الميزة اللي كانت ناقصة)
        table_frame = ctk.CTkFrame(self.main_content)
        table_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Category", "Amount", "Date"), show='headings')
        self.tree.heading("ID", text="م")
        self.tree.heading("Category", text="الفئة")
        self.tree.heading("Amount", text="المبلغ")
        self.tree.heading("Date", text="التاريخ")
        
        # تصليح الـ width اللي كان عامل مشكلة
        self.tree.column("ID", width=50)
        self.tree.column("Category", width=200)
        self.tree.column("Amount", width=100)
        
        self.tree.pack(fill="both", expand=True)

        self.chart_btn = ctk.CTkButton(self.sidebar, text="تحديث الرسم البياني", command=self.show_chart)
        self.chart_btn.pack(pady=10, padx=10)

    def add_expense(self):
        cat = self.category_entry.get()
        amt = self.amount_entry.get()
        date = datetime.now().strftime("%Y-%m-%d")
        if cat and amt:
            self.cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (cat, amt, date))
            self.conn.commit()
            self.load_data()
            self.category_entry.delete(0, 'end')
            self.amount_entry.delete(0, 'end')

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM expenses")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def show_chart(self):
        self.cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = self.cursor.fetchall()
        if data:
            categories = [d[0] for d in data]
            amounts = [d[1] for d in data]
            plt.figure("تحليل المصاريف")
            plt.pie(amounts, labels=categories, autopct='%1.1f%%')
            plt.show()

if __name__ == "__main__":
    app_root = ctk.CTk()
    app = ExpenseApp(app_root)
    app_root.mainloop()
