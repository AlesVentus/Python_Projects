import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import ttk
import requests
import os
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import itertools
from Setup import get_pass


window = tk.Tk()
window.title("API form")
window.rowconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=800, weight=1)


CheckVar1 = StringVar()
CheckVar2 = StringVar()
CheckVar3 = StringVar()
CheckVar4 = StringVar()
CheckVar5 = StringVar()

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

def API_url():
    #get url from form
    lang = Lb1.get(Lb1.curselection())
    url = "https://api.stackexchange.com//2.3/questions?order=desc&sort=creation&tagged=" + lang + "&site=stackoverflow&pagesize=10"
    return url


def API_language():
    #get language from form
    return Lb1.get(Lb1.curselection())
     

def API_columns():
    #dynamicaly create string used in API to extract columns selected in form
    api_columns = "[str(question[\'title\'])"
    list_var = ['CheckVar' + str(i) for i in range(1,6)]
    for var in list_var:
        if globals()[var].get() != 'off':
            api_columns += "," + "str(question[\'" + globals()[var].get() + "\'])"
    api_columns = api_columns + ']'

    return api_columns


def Tree_columns():
    #create list of selected columns in form
    tree_columns = ['title']
    list_var = ['CheckVar' + str(i) for i in range(1,6)]
    for var in list_var:
        if globals()[var].get() != 'off':
            tree_columns.append(globals()[var].get())

    return tree_columns


def API_Connect():
    
    url = API_url()
    columns = API_columns()
    #tree_cols = Tree_columns()
    query_result = []

    r = requests.get(url)
    r_dict = r.json()

    # dynamically created list of columns is read from json - eval(columns)
    for question in r_dict["items"]:
        query_result.append(eval(columns))

    return query_result

####################################################
                 #CLASS
####################################################

class API_content:

    def __init__(self):
        self.api_result = []
        self.language = ''
        self.txt_query_result = ''
        self.pdf_query_result = ''
        self.tree_columns = []
        self.tree_columns = ''


    def get_txt_query_result(self):
        #change bool to str
        changes = { True: "True",False: "False"}
        to_string = []
        #change inner list to string using join
        for item in self.api_result:
            item = [ changes.get( x, x ) for x in item ]
            to_string.append(item)   

        return [",".join( map( str, x ) ) for x in to_string]
        


    def API_content(self):   

        tree_api['columns'] = Tree_columns()

        url = API_url()
        self.language = API_language() 
        self.api_result = API_Connect()
        self.txt_query_result = '\n'.join(self.get_txt_query_result())
        self.pdf_query_result = self.get_txt_query_result()
        self.tree_columns =  Tree_columns()

        #create treeview widget
        # fantome column in treeview
        tree_api.column('#0', width=0, stretch=NO)
        tree_api.heading('#0', text='')

        for column in self.tree_columns:
            tree_api.column(column, width=80)
            tree_api.heading(column, text=column)

        tree_api.delete(*tree_api.get_children())
        indexing = 0
        
        for result in self.api_result:
            tree_api.insert(parent='', index='end', iid=indexing, text='', values=result)
            indexing += 1


    def Save_As(self):
        if len(self.txt_query_result) > 0:
            with open(desktop + '\\test.txt', 'w', encoding='utf-8') as f:
                f.write(str(self.txt_query_result))
                msgbox.showinfo('saving data', 'Data successfuly saved')
        else:
            msgbox.showinfo('saving data', 'No data for saving')


    def print_PDF(self):

        if len(self.pdf_query_result) > 0:

            line = 3
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size = 14)
            
            # create a cell
            pdf.cell(200, 10, txt = self.language,ln = 1, align = 'C', border=1)
            pdf.cell(200, 10, txt = "Data from https://api.stackexchange.com",ln = 2, align = 'C', link='https://stackoverflow.com/')

            pdf.set_font("Arial", size = 10)
            for res in self.pdf_query_result:
                pdf.cell(200, 10, txt = res, ln = line, align = 'L')
                line += 1

            pdf.output(desktop + "\\test.pdf") 
            msgbox.showinfo('print PDF', 'Data successfuly printed')

        else:
            msgbox.showinfo('print PDF', 'No data for PDF')


    def send_email(self):
        
        mail_pass = get_pass.get_password()
        mail_user = 'alesventus@gmail.com'

        if len(self.txt_query_result) > 0:
            msg = EmailMessage()
            msg['From'] = 'training team Ales'
            msg['To'] = 'alesventus@gmail.com'
            msg['Subject'] = self.language + ' results:'
            msg.set_content(self.txt_query_result)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(mail_user, mail_pass)
            server.send_message(msg)

            server.quit()
            msgbox.showinfo('send email', 'Data successful sent')

        else:
            msgbox.showinfo('send email', 'No data for email')

####################################################
                 #end CLASS
####################################################

api_obj = API_content()

tree_api = ttk.Treeview(window)
fr_menu = tk.Frame(window, relief=tk.RAISED)
lbl_option = tk.Label(fr_menu, text="select language:")
lbl_column = tk.Label(fr_menu, text="output columns:")
btn_result = tk.Button(fr_menu, text="API results", width = 25, command = api_obj.API_content)
btn_save = tk.Button(fr_menu, text="Save As...", command = api_obj.Save_As)
btn_print = tk.Button(fr_menu, text="Print to PDF", command = api_obj.print_PDF)
btn_email = tk.Button(fr_menu, text="Email results", command = api_obj.send_email)


Lb1 = Listbox(fr_menu, height=3,selectmode='SINGLE')
Lb1.insert(1, "Python")
Lb1.insert(2, "Powershell")
Lb1.insert(2, "SQL")
Lb1.selection_set( first = 0 )


chk_answered = Checkbutton(fr_menu, text='answered', variable = CheckVar1, onvalue='is_answered', offvalue='off')
chk_answer_count = Checkbutton(fr_menu, text='answer_count', variable = CheckVar2, onvalue='answer_count', offvalue='off')
chk_view_count = Checkbutton(fr_menu, text='view_count', variable = CheckVar3, onvalue='view_count', offvalue='off')
chk_score = Checkbutton(fr_menu, text='score', variable = CheckVar4, onvalue='score', offvalue='off')
chk_creation_date = Checkbutton(fr_menu, text='creation_date', variable = CheckVar5, onvalue='creation_date', offvalue='off')


chk_answered.deselect()
chk_answer_count.deselect()
chk_view_count.deselect()
chk_score.deselect()
chk_creation_date.deselect()


btn_result.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_print.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_email.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
lbl_option.grid(row=4, column=0)
Lb1.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

lbl_column.grid(row=6, column=0, sticky="ew", padx=5)
chk_answered.grid(row=7, column=0, sticky="w", padx=5)
chk_answer_count.grid(row=8, column=0, sticky="w", padx=5)
chk_view_count.grid(row=9, column=0, sticky="w", padx=5)
chk_score.grid(row=10, column=0, sticky="w", padx=5)
chk_creation_date.grid(row=11, column=0, sticky="w", padx=5)


fr_menu.grid(row=0, column=0, sticky="ns")
tree_api.grid(row=0, column=1, sticky="nsew")


window.mainloop()