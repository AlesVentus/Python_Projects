import json

path_file = "C:\\Coding\\Python\\Python_Projects\\01_API_Form\\Email_Setup\\data\\data.txt"

def get_json_data():

    json_data = []
    with open(path_file) as json_file:
        data = json.load(json_file)

        for p in data['email_setting']:
            content_account = p['account']
            content_from_mail = p['from_mail']
            content_send_to = p['send_to']
            content_smtp_server = p['smtp_server']
            content_smtp_password = p['smtp_password']
    return content_account, content_from_mail, content_send_to, content_smtp_server, content_smtp_password