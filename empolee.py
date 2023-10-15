import sqlite3
import tkinter as tk
from tkinter import ttk

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(background='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.BOTH)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.btn_open_dialog = tk.Button(toolbar, background='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        self.btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview (self, columns=('id', 'name', 'phone', 'email', 'salary'), height=45, show='headings')

        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=100, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Full name')
        self.tree.heading('phone', text='Telephone number')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Salary')

        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file = './img/update.png')
        btn_edit_dialog = tk.Button(toolbar, background='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file = './img/delete.png')
        btn_delete_dialog = tk.Button(toolbar, background='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file = './img/search.png')
        btn_search_daylog = tk.Button(toolbar, background='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search_daylog.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file = './img/refresh.png')
        btn_refresh_dialog = tk.Button(toolbar, background='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh_dialog.pack(side=tk.LEFT)

    def open_dialog(self):
        Child()

    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    def view_records(self):
        self.db.cursor.execute('SELECT * FROM employee')

        [self.tree.delete(value) for value in self.tree.get_children()]

        [self.tree.insert('', 'end', values = row) for row in self.db.cursor.fetchall()]

    def open_update_dialog(self):
        Update()

    def update_record(self, name, phone, email, salary):
        self.db.cursor.execute('''UPDATE employee SET name=?, phone=?, email=?, salary=? WHERE id=?''', (name, phone, email, salary, self.tree.set(self.tree.selection() [0], '#1')),)
        self.db.connect.commit()
        self.view_records()

    def delete_record(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('DELETE FROM employee WHERE id=?', (self.tree.set(selection_item, '#1')))
        
        self.db.connect.commit()
        self.view_records()

    def open_search_dialog(self):
        Search()

    def search_record(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute('SELECT * FROM employee WHERE name LIKE ?', (name,)) # Передача кортежа (name,), а не просто name
        
        [self.tree.delete(value) for value in self.tree.get_children()]
        
        [self.tree.insert('', 'end', values = row) for row in self.db.cursor.fetchall()]

class Child(tk.Toplevel): # Дочернее окно (добавление шуток) !
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить запись')
        self.geometry('400x230')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set() # Фокусировка

        label_name = tk.Label(self, text='Full name')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Telephone number')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Salary')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_good = ttk.Button(self, text='Добавить')
        self.btn_good.place(x=220, y=170)

        self.btn_good.bind('<Button-1>', lambda event:
                           self.view.records(self.entry_name.get(),
                                             self.entry_phone.get(),
                                             self.entry_email.get(),
                                             self.entry_salary.get()),)

class Update(Child): # Дочернее окно (изменение шуток) !
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Изменение текущего сотрудника !')
        btn_edit = ttk.Button(self, text = 'Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_phone.get(),
                                              self.entry_email.get(),
                                              self.entry_salary.get()),) # Отслеживание левой кнопки мыши + добавление вхождений
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add = '+') # Отслеживание ЛКМ + закрытие окна
        self.btn_good.destroy()

    def default_data(self):
        self.db.cursor.execute('SELECT * FROM employee WHERE id=?', (self.view.tree.set(self.view.tree.selection() [0], '#1')))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel): # Код, отвечающий за поиск контакта в ежедневнике !
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск сотрудника !')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Полное имя')
        label_search.place(x=10, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Выполнить поиск')
        btn_search.place(x=70, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_record(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class DB(): # Создание базы данных !
    def __init__(self):
        self.connect = sqlite3.connect('employee.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employee (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            salary TEXT
        );
        ''')
        self.connect.commit()

    def insert_data(self, name, phone, email, salary):
        self.cursor.execute('''INSERT INTO employee (name, phone, email, salary) VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.connect.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Employee')
    root.geometry('800x500')
    root.resizable(False, False)
    root.mainloop()