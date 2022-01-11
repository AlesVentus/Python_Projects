from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("500x500")

my_tree = ttk.Treeview(root)

column_name = ['is_answered', 'answer_count', 'view_count']
data = [['jimmy', '100', 'Tulsa']]

my_tree['columns'] = column_name

# fantome column
my_tree.column('#0', width=0, stretch=NO)
my_tree.heading('#0', text='')

for column in column_name:
    my_tree.column(column, width=80)
    my_tree.heading(column, text=column)


my_tree.insert(parent='', index='end', iid=0, text='', values=(data[0][0], data[0][1], data[0][2]))


my_tree.grid()



root.mainloop()