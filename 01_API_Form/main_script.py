import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import *
import requests
import os
from fpdf import FPDF


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
txt_query_result = ''

#test method only
def helloCallBack():
    #get listbox value
    selection=Lb1.curselection()
    value = Lb1.get(selection[0])

    #get checked checkboxes
    result = ''
    list_var = ['CheckVar' + str(i) for i in range(1,6)]
    for var in list_var:
        if globals()[var].get() != 'off':
            result = result + globals()[var].get() + '\n'
        
    msgbox.showinfo( "Hello API", "You selected: " + str(value) + '\n' + result)


def API_string():

    lang = Lb1.get(Lb1.curselection())
    url = "https://api.stackexchange.com//2.3/questions?order=desc&sort=creation&tagged=" + lang + "&site=stackoverflow&pagesize=10"
    return url


def API_cols():

    cols_result = "str(question[\'title\'])"
    list_var = ['CheckVar' + str(i) for i in range(1,6)]
    for var in list_var:
        if globals()[var].get() != 'off':
            cols_result += " + \'--\' + str(question[\'" + globals()[var].get() + "\'])"

    return cols_result


def API_content():

    url = API_string()
    columns = API_cols()

    global txt_query_result 
    global query_result 
    query_result = []

    r = requests.get(url)
    r_dict = r.json()

    txt_api.delete('1.0', END)
    # dynamically created list of columns is read from json - eval(columns)
    for question in r_dict["items"]:
        query_result.append(eval(columns))
   
    txt_query_result = '\n'.join(query_result)
    txt_api.insert(1.0, txt_query_result)
    txt_api.update()


def SaveAs():

    if len(txt_query_result) > 0:
        with open(desktop + '\\test.txt', 'w', encoding='utf-8') as f:
            f.write(str(txt_query_result))
            msgbox.showinfo('saving data', 'Data successfuly saved')
    else:
        msgbox.showinfo('saving data', 'No data for saving')


def Print_PDF():

    line = 3
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 14)
    
    # create a cell
    pdf.cell(200, 10, txt = "API Export",ln = 1, align = 'C', border=1)
    pdf.cell(200, 10, txt = "Data from https://api.stackexchange.com",ln = 2, align = 'C', link='https://stackoverflow.com/')

    pdf.set_font("Arial", size = 10)
    for res in query_result:
        pdf.cell(200, 10, txt = res, ln = line, align = 'L')
        line += 1

    pdf.output(desktop + "\\test.pdf") 

txt_api = tk.Text(window)
fr_menu = tk.Frame(window, relief=tk.RAISED)
lbl_option = tk.Label(fr_menu, text="select language:")
lbl_column = tk.Label(fr_menu, text="output columns:")
btn_result = tk.Button(fr_menu, text="API results", width = 25, command = API_content)
btn_save = tk.Button(fr_menu, text="Save As...", command = SaveAs)
btn_print = tk.Button(fr_menu, text="Print to PDF", command = Print_PDF)
btn_email = tk.Button(fr_menu, text="Email results", command = helloCallBack)
btn_properties = tk.Button(fr_menu, text="Properties", command = helloCallBack)


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
txt_api.grid(row=0, column=1, sticky="nsew")


window.mainloop()