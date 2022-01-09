from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import requests



class API_content:

    def __init__(self):
        self.api_result = ''
        self.language = 'test language'
        self.txt_query_result = ''
        self.query_result = []

    def API_content(self):

        url, self.language = API_url()
        columns = API_columns()
        self.query_result = []

        r = requests.get(url)
        r_dict = r.json()

        txt_api.delete('1.0', END)
        # dynamically created list of columns is read from json - eval(columns)
        for question in r_dict["items"]:
            self.query_result.append(eval(columns))
    
        self.txt_query_result = '\n'.join(self.query_result)
        txt_api.insert(1.0, self.txt_query_result)
        txt_api.update()


    def Save_As(self):
        if len(self.txt_query_result) > 0:
            with open(desktop + '\\test.txt', 'w', encoding='utf-8') as f:
                f.write(str(self.txt_query_result))
                msgbox.showinfo('saving data', 'Data successfuly saved')
        else:
            msgbox.showinfo('saving data', 'No data for saving')


    def print_PDF(self):

        if len(self.query_result) > 0:

            line = 3
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size = 14)
            
            # create a cell
            pdf.cell(200, 10, txt = self.language,ln = 1, align = 'C', border=1)
            pdf.cell(200, 10, txt = "Data from https://api.stackexchange.com",ln = 2, align = 'C', link='https://stackoverflow.com/')

            pdf.set_font("Arial", size = 10)
            for res in self.query_result:
                pdf.cell(200, 10, txt = res, ln = line, align = 'L')
                line += 1

            pdf.output(desktop + "\\test.pdf") 
            msgbox.showinfo('print PDF', 'Data successfuly printed')

        else:
            msgbox.showinfo('print PDF', 'No data for PDF')


    def get_password(self):

        with open(pass_path, 'r') as f:
            return f.read()


    def send_email(self):
        
        mail_pass = self.get_password()
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