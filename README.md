# bitwarden-pdf-converter

Put your bitwarden export .json file in the resources directory and rename it to password.json.

Then run `bitwarden_pdf_converter.py` in the terminal.

## Installation

### HTML Export

Run the following commands in your terminal

```bash
pip install jinja2
pip install json
python bitwarden_html_converter.py
```

### PDF Export

Run the following commands in your terminal

```bash
pip install pdfkit
pip install jinja2
pip install json
```

For windows install [wkhtmltopdf](https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_msvc2015-win64.exe)

Add the path to the wkhtmltopdf executable to your PATH environment variable.

For Linux run `sudo apt-get install wkhtmltopdf`

```bash
python bitwarden_pdf_converter.py
```
