pass_path = 'C:\\Coding\\Python\\Python_Projects\\01_API_Form\\Setup\\pass.txt'

def get_password():

    with open(pass_path, 'r') as f:
        return f.read()