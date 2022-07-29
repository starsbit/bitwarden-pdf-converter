'''
    convert bitwarden export to html
'''

from glob import glob
from os.path import exists, join
import json
from jinja2 import Environment


TEMPLATE = '''<!DOCTYPE html>
<html lang="en" class="extdovdh idc0_341">
  <head>
    <title>My Vault</title>
    <meta charset="utf-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />
    <!-- Latest compiled and minified CSS -->
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css"
      integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu"
      crossorigin="anonymous"
    />

    <!-- Optional theme -->
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap-theme.min.css"
      integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ"
      crossorigin="anonymous"
    />

    <!-- Latest compiled and minified JavaScript -->
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/js/bootstrap.min.js"
      integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd"
      crossorigin="anonymous"
    ></script>
  </head>
  <body>
    <h1>My Vault</h1>
    <section class="ftco-section">
      <div class="container">
        {% for category in categories %}
        <div class="row justify-content-center">
          <div class="col-md-6 text-center mb-5">
            <h2 class="heading-section">{{ category.name }}</h2>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="table-wrap">
              <table class="table table-bordered table-dark table-hover">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Note</th>
                    <th>Username</th>
                    <th>Password</th>
                    <th>URL</th>
                  </tr>
                </thead>

                <tbody>
                  {% for item in category["items"] %}
                  <tr>
                    <td>{{ item.name }}</td>
                    <td>{{ item.notes }}</td>
                    <td>{{ item.username }}</td>
                    <td>{{ item.password }}</td>
                    <td>{{ item.url }}</td>
                  </tr>
                  {% endfor %}
                </tbody>
              </table>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
    </section>
  </body>
</html>
'''


def get_password_file_name():
    '''
    Returns the name of the password file
    '''
    possibilities = ['./resources/password.json', './password.json']
    for possibility in possibilities:
        if exists(possibility):
            return possibility

    other_findings = []

    other_findings.append(glob(join('./resources', 'bitwarden*.json')))
    other_findings.append((glob('./bitwarden*.json')))

    if len(other_findings[0]) != 0:
        return other_findings[0][0].replace('\\', '/')
    elif len(other_findings[1]) != 0:
        return other_findings[1][0].replace('\\', '/')
    else:
        raise FileNotFoundError("No password file found")


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
    env = Environment()

    loaded_template = env.from_string(TEMPLATE)
    categories = []
    unrelated_category = {'name': 'Uncategorized', 'items': []}
    categories.append(unrelated_category)

    with open(get_password_file_name(), 'r', encoding="utf-8") as bitwarden_file:
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

    return loaded_template.render(categories=categories)


with open('./resources/output.html', 'w', encoding="utf-8") as html_file:
    html_file.write(parse_to_html())
