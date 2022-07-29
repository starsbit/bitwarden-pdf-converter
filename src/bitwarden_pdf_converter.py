'''
    Parses the bitwarden.json file and converts the PDFs to PNGs.
'''
import pdfkit

from bitwarden_html_converter import parse_to_html

pdfkit.from_string(parse_to_html(), './resources/output.pdf')
