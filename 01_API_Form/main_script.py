import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import *
import requests

window = tk.Tk()
window.title("API form")
window.rowconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=800, weight=1)


CheckVar1 = StringVar()
CheckVar2 = StringVar()
CheckVar3 = StringVar()
CheckVar4 = StringVar()
CheckVar5 = StringVar()


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

    result = "str(question[\'title\'])"
    list_var = ['CheckVar' + str(i) for i in range(1,6)]
    for var in list_var:
        if globals()[var].get() != 'off':
            result += " + \'--\' + str(question[\'" + globals()[var].get() + "\'])"

    msgbox.showinfo( "Hello API",result)
    return result

def API_content():

    url = API_string()
    columns = API_cols()

    r = requests.get(url)
    r_dict = r.json()

    txt_api.delete('1.0', END)

    for question in r_dict["items"]:
        item = eval(columns)
        txt_api.insert(1.0, item + '\n')
   
    txt_api.update()
    

txt_api = tk.Text(window)
fr_menu = tk.Frame(window, relief=tk.RAISED)
lbl_option = tk.Label(fr_menu, text="select content:")
btn_result = tk.Button(fr_menu, text="API results", width = 25, command = API_content)
btn_save = tk.Button(fr_menu, text="Save As...", command = helloCallBack)
btn_print = tk.Button(fr_menu, text="Print to PDF", command = helloCallBack)
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


chk_answered.grid(row=6, column=0, sticky="w", padx=5)
chk_answer_count.grid(row=7, column=0, sticky="w", padx=5)
chk_view_count.grid(row=8, column=0, sticky="w", padx=5)
chk_score.grid(row=9, column=0, sticky="w", padx=5)
chk_creation_date.grid(row=10, column=0, sticky="w", padx=5)


fr_menu.grid(row=0, column=0, sticky="ns")
txt_api.grid(row=0, column=1, sticky="nsew")


window.mainloop()