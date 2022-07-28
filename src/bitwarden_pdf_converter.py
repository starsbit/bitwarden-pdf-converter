'''
    Parses the bitwarden.json file and converts the PDFs to PNGs.
'''
import json

import pdfkit
from jinja2 import Environment, FileSystemLoader, select_autoescape


def check_field(bitwarden_item, field):
    '''
    Checks if a field is present in the bitwarden item and applies default value if not
    '''
    try:
        return bitwarden_item[field]
    except KeyError:
        return None


def parse_item(bitwarden_item):
    '''
    Converts bitwarden syntax to intern syntax
    '''
    i_item = {}
    i_item["name"] = check_field(bitwarden_item, "name")
    i_item["notes"] = check_field(bitwarden_item, "notes")
    login = check_field(bitwarden_item, "login")
    if login:
        i_item["username"] = check_field(login, "username")
        i_item["password"] = check_field(login, "password")
    try:
        i_item["url"] = bitwarden_item["login"]["uris"][0]["uri"]
    except (KeyError, IndexError):
        i_item["url"] = None
    return i_item


env = Environment(
    loader=FileSystemLoader('src/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
categories = []
unrelatedCategory = {'name': 'Uncategorized', 'items': []}
categories.append(unrelatedCategory)

with open('./resources/password.json', 'r', encoding="utf-8") as f:
    data = json.load(f)
    for folder in data["folders"]:
        folderId = folder["id"]
        folderName = folder["name"]
        category = {}
        category["items"] = []
        category["name"] = folderName
        for item in data["items"]:
            if item["folderId"] == folderId:
                category["items"].append(parse_item(item))
        categories.append(category)
    for item in data["items"]:
        if item["folderId"] is None:
            unrelatedCategory["items"].append(parse_item(item))

html = template.render(categories=categories)

with open('./resources/output.html', 'w', encoding="utf-8") as f:
    f.write(html)

pdfkit.from_string(html, './resources/output.pdf')
