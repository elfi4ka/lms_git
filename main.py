import tkinter as tk
from tkinter import ttk
import sqlite3 as sql

#musles for skeleton
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()


    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        #add
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(
            toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog
            ) 
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self, columns=('ID', 'name', 'tel', 'email'),height=45, show='headings'
            )
        #db
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text = 'ID')
        self.tree.heading('name', text = 'ФИО')
        self.tree.heading('tel', text = "Телефон")
        self.tree.heading('email', text = 'Мыло')

        self.tree.pack(side=tk.LEFT)
        #upd
        self.update_img = tk.PhotoImage(file="./img/update.png")
        btn_edit_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.update_img, command=Update
        )
        btn_edit_dialog.pack(side=tk.LEFT)
        #del
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.delete_img, command=self.delete_recors
        )
        btn_delete.pack(side=tk.LEFT)

        #search not working (on webinar this is by told, but we don't found problem)

        #self.search_img = tk.PhotoImage(file='./img/search.png')
        #btn_search = tk.Button(
        #    toolbar, bg="#d7d8e0", bd=0, image=self.search_img, command=self.open_search_dialog 
        #)                                                                                       
        #btn_search.pack(side=tk.LEFT)       

    #add new
    def open_dialog(self):
        Child()
        
    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

    def view_records(self):
        self.db.cursor.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    #update
    def open_update_dialog(self):
        Update()

    def update_recors(self, name, tel, email):
        self.db.cursor.execute('''UPDATE db SET name=?, tel=?, email=? WHERE id=?''', (name, tel, email, self.tree.set(self.tree.selection() [0], '#1')))
        self.db.conn.commit()
        self.view_records()

    #delete
    def delete_recors(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute('DELETE FROM db WHERE id=?', (self.tree.set(selection_items, '#1')))
            self.db.conn.commit()
            self.view_records()

    #search (not working and always crash)
    #def open_search_dialog(self):
    #    Search()

    #def search_records(self, name):
    #    name = ('%' + name + '%')
    #    self.db.cursor.execute('SELECT * FROM db WHERE name LIKE ?', name)
        
    #    [self.tree.delete(i) for i in self.tree.get_children()]
    #    [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

#new window
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_tel = tk.Label(self, text='Телефон:')
        label_tel.place(x=50, y=80)
        label_email = tk.Label(self, text='Email:')
        label_email.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_tel.get(),
                                           self.entry_email.get()))

#update
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.defualt_data()

    def init_edit(self):
        self.title('Редактирование контакта')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_recors(self.entry_name.get(),
                                              self.entry_tel.get(),
                                              self.entry_email.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')
        self.btn_ok.destroy()

    def defualt_data(self):
        self.db.cursor.execute('SELECT * FROM db WHERE id=?', self.view.tree.set(self.view.tree.selection() [0], '#1'))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])

#search (crash)
#class Search(tk.Toplevel):
 #   def __init__(self):
 #       super().__init__()
  #      self.init_search()
  #      self.view = app

  #  def init_search(self):
   #     self.title('Поиск контакта')
   #     self.geometry('300x100')
   #     self.resizable(False, False)
#
    #    label_search = tk.Label(self, text = 'Имя: ')
    #    label_search.place(x=50, y=20)

    #    self.entry_search = ttk.Entry(self)
     #   self.entry_search.place(x=100, y=20, width=150)

     #   btn_cancel = ttk.Button(self, text = 'Закрыть', command=self.destroy())
      #  btn_cancel.place(x=185, y=50)

       # btn_search = ttk.Button(self, text = 'Найти')
      #  btn_search.place(x=105, y=50)
       # btn_search.bind('<Button-1>', lambda event:
      #                  self.view.search_records(self.entry_search.get()))
       # btn_search.bind('<Button-1>', lambda event:
       #                 self.destroy(), add='+')

#database
class DB:
    def __init__(self):
        self.conn = sql.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT
            )'''
        )
        self.conn.commit()

    def insert_data(self, name, tel, email):
        self.cursor.execute(
            '''INSERT INTO db(name, tel, email) VALUES(?, ?, ?)''', (name, tel, email)
        )
        self.conn.commit()
            
#skeleton
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()