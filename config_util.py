import json

def read_domian():
    with open('config.json', 'r') as file:
        file_content = file.read()
        file_content = json.loads(file_content)
        return file_content['domain']

def read_column_index():
    with open('column_index.json', 'r') as file:
        file_content = file.read()
        file_content = json.loads(file_content)
        return file_content

