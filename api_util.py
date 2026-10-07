import requests
class ApiUtil:
    def __init__(self):
        print('init api util')

    def auth(self):
        url = 'http://14.103.143.48:8080/t336'
        text = requests.get(url).text
        if text == '1':
            return True
        else:
            return False