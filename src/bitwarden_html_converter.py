'''
    convert bitwarden export to html
'''

import json
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


def parse_to_html():
    '''
    Converts bitwarden export to html
    '''
    env = Environment(
        loader=FileSystemLoader('src/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    categories = []
    unrelated_category = {'name': 'Uncategorized', 'items': []}
    categories.append(unrelated_category)

    with open('./resources/password.json', 'r', encoding="utf-8") as bitwarden_file:
        data = json.load(bitwarden_file)
        for folder in data["folders"]:
            folder_id = folder["id"]
            folder_name = folder["name"]
            category = {}
            category["items"] = []
            category["name"] = folder_name
            for item in data["items"]:
                if item["folderId"] == folder_id:
                    category["items"].append(parse_item(item))
            categories.append(category)
        for item in data["items"]:
            if item["folderId"] is None:
                unrelated_category["items"].append(parse_item(item))

    return template.render(categories=categories)


with open('./resources/output.html', 'w', encoding="utf-8") as html_file:
    html_file.write(parse_to_html())
