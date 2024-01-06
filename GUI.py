from tkinter import *
from SQLite import LibDB
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter import messagebox
import csv

class LibraryGuiTk(Tk):

    def __init__(self, dataBase=LibDB('Library.db')):
        super().__init__()
        self.db = dataBase
        self.title('Library Database System')
        self.geometry('1060x600')
        self.config(bg='#161C25')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Book ID', 'Author', 'Title', 'Genre', 'Availability')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Book ID', anchor=tk.CENTER, width=10)
        self.tree.column('Author', anchor=tk.CENTER, width=100)
        self.tree.column('Title', anchor=tk.CENTER, width=150)
        self.tree.column('Genre', anchor=tk.CENTER, width=10)
        self.tree.column('Availability', anchor=tk.CENTER, width=150)

        self.tree.heading('Book ID', text='Book ID')
        self.tree.heading('Author', text='Author')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Availability', text='Availability')

        self.tree.place(x=30, y=20, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

        self.id_label = self.newCtkLabel('Book ID')
        self.id_label.place(x=50, y=400)
        self.id_entryVar = StringVar()
        self.id_entry = self.newCtkEntry(entryVariable=self.id_entryVar)
        self.id_entry.place(x=100, y=400)

        self.author_label = self.newCtkLabel(' Author ')
        self.author_label.place(x=50, y=430)
        self.author_entryVar = StringVar()
        self.author_entry = self.newCtkEntry(entryVariable=self.author_entryVar)
        self.author_entry.place(x=101, y=430)

        self.title_label = self.newCtkLabel('   Title    ')
        self.title_label.place(x=50, y=460)
        self.title_entryVar = StringVar()
        self.title_entry = self.newCtkEntry(entryVariable=self.title_entryVar)
        self.title_entry.place(x=100, y=460)

        self.genre_label = self.newCtkLabel('  Genre  ')
        self.genre_label.place(x=50, y=490)
        self.genre_entryVar = StringVar()
        self.genre_entry = self.newCtkEntry(entryVariable=self.genre_entryVar)
        self.genre_entry.place(x=100, y=490)

        self.status_label = self.newCtkLabel('  Status  ')
        self.status_label.place(x=50, y=520)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Available', 'Borrowed', 'Out of Stock']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=520)

        self.add_button = self.newCtkButton(text='Add Book',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=375,y=410)

        self.add_button = self.newCtkButton(text='Update Book',
                                onClickHandler=self.update_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=375,y=470)

        self.add_button = self.newCtkButton(text='Delete Book',
                                onClickHandler=self.delete_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=570,y=410)

        self.add_button = self.newCtkButton(text='Export .csv',
                                onClickHandler=self.export_to_csv,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=570,y=470)

        self.add_button = self.newCtkButton(text='Export .json',
                                onClickHandler=self.export_to_json,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=765,y=410)

        self.add_button = self.newCtkButton(text='Import .csv',
                                onClickHandler=self.import_csv,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=765,y=470)



    def add_to_treeview(self):
        books = self.db.fetch_entry()
        self.tree.delete(*self.tree.get_children())
        for books in books:
            print(books)
            self.tree.insert('', END, values=books)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entryVar.set('')
        self.author_entryVar.set('')
        self.title_entryVar.set('')
        self.genre_entryVar.set('')
        self.status_cboxVar.set('Available')

    def add_entry(self):
        id=self.id_entryVar.get()
        author=self.author_entryVar.get()
        title=self.title_entryVar.get()
        genre=self.genre_entryVar.get()
        status=self.status_cboxVar.get()

        if not (id and author and title and genre and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_entry(id, author, title, genre, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entryVar.set(row[0])
            self.author_entryVar.set(row[1])
            self.title_entryVar.set(row[2])
            self.genre_entry.set(row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to delete')
        else:
            id = self.id_entryVar.get()
            self.db.delete_entry(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.process_csv(file_path)

    def process_csv(self, file_path):
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            try:
                header = next(csv_reader)
            except StopIteration:
                messagebox.showwarning('Empty CSV', 'The selected CSV file is empty.')
                return
            data = [row for row in csv_reader]
            for row in data:
                self.tree.insert("", "end", values=row)         

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an employee to update')
        else:
            id=self.id_entryVar.get()
            name=self.author_entryVar.get()
            role=self.title_entryVar.get()
            gender=self.genre_entryVar.get()
            status=self.status_cboxVar.get()
            self.db.update_entry(name, role, gender, status, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')
    
    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.json')

    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = ttk.Label(self, 
                        text=text)
        return widget
    
    def newCtkEntry(self, text = 'CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget
    
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25
        widget_Options=options

        widget = ttk.Combobox(self, 
                              textvariable=entryVariable,
                              width=widget_Width)
        widget['values'] = tuple(options)
        widget.current(1)
        return widget

    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
                            width=widget_Width)
       
        return widget