import tkinter as tk
from tkinter.constants import END
from tkinter import messagebox
import json
from typing import Text
from Email_Setup import Read_json


class Email_Form:

    path_file = "C:\\Coding\\Python\\Python_Projects\\01_API_Form\\Email_Setup\\data\\data.txt"

    def __init__(self):

        self.account = ''
        self.from_mail = ''
        self.send_to = ''
        self.smtp_server = ''
        self.smtp_password = ''

        self.subroot = tk.Tk()
        self.subroot.title('email notification settings')

        self.lbl_account = tk.Label(self.subroot, text="Account: ")
        self.lbl_from = tk.Label(self.subroot, text="From: ")
        self.lbl_to = tk.Label(self.subroot, text="To: ")
        self.lbl_smtp_server = tk.Label(self.subroot, text="SMTP Server:")
        self.lbl_smtp_password = tk.Label(self.subroot, text="SMTP password:")


        self.ent_account = tk.Entry(self.subroot, width=45)
        self.ent_send_from = tk.Entry(self.subroot)
        self.ent_send_to = tk.Entry(self.subroot)
        self.ent_smtp_server = tk.Entry(self.subroot)
        self.ent_smtp_password = tk.Entry(self.subroot, show="*")

        self.btn_OK = tk.Button(self.subroot, text="OK", command=self.accept_data)

        self.lbl_account.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.lbl_from.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.lbl_to.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.lbl_smtp_server.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.lbl_smtp_password.grid(row=4, column=0, sticky="e", padx=5, pady=5)

        self.ent_account.grid(row=0, column=1, sticky="ewns", padx=5, pady=5, columnspan=2)
        self.ent_send_from.grid(row=1, column=1, sticky="ewns", padx=5, pady=5, columnspan=2)
        self.ent_send_to.grid(row=2, column=1, sticky="ewns", padx=5, pady=5, columnspan=2)
        self.ent_smtp_server.grid(row=3, column=1, sticky="ewns", padx=5, pady=5, columnspan=2)
        self.ent_smtp_password.grid(row=4, column=1, sticky="ewns", padx=5, pady=5, columnspan=2)

        self.btn_OK.grid(row=5, column=1, sticky="ewns", padx=5, pady=5)


        # json from module 
        content_account, content_from_mail, content_send_to, content_smtp_server,content_smtp_password  = Read_json.get_json_data()

        self.ent_account.insert(0, content_account)
        self.ent_send_from.insert(0, content_from_mail)
        self.ent_send_to.insert(0, content_send_to)
        self.ent_smtp_server.insert(0, content_smtp_server)
        self.ent_smtp_password.insert(0, content_smtp_password)

        self.subroot.attributes('-topmost',True)
        self.subroot.mainloop()


    def accept_data(self):

        MsgBox = messagebox.askquestion('email settings:', 'Do you want to save changes?', master=self.subroot)

        if MsgBox == 'yes':
            self.save_json()
            self.subroot.destroy()
        else:
            self.subroot.destroy()


    def save_json(self):

        data = {}
        data['email_setting'] = []
        data['email_setting'].append({
            'account': self.ent_account.get(),
            'from_mail': self.ent_send_from.get(),
            'send_to': self.ent_send_to.get(),
            'smtp_server': self.ent_smtp_server.get(),
            'smtp_password': self.ent_smtp_password.get()
        })


        with open(self.path_file, 'w') as outfile:
            json.dump(data, outfile)



def email_frm():
    display = Email_Form()


if __name__ == "__main__":
    email_frm()
