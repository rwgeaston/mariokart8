#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cgitb
from cgi import FieldStorage
#enable debugging
cgitb.enable()

from html_tools import bold, paragraph, html_table

GET = FieldStorage()


def print_page(title, page_content):
    print '''Content-Type: text/html
<html>
<head>
<title>MK8: {}</title>
</head>
'''.format(title)
    for section_type, section_content in page_content:
        if section_type == 'table':
            print html_table(section_content)
        elif section_type == 'text':
            print paragraph(section_content)
        elif section_type == 'important text':
            print bold(paragraph(section_content))
        else:
            raise Exception(
                "I don't know how to deal with this type of content: {}"
                .format(section_type)
            )


def get_form_values(expected_form_variables):
    form_values = {}
    for variable, default_value, expected_type in expected_form_variables:
        if variable in GET:
            try:
                form_values[variable] = expected_type(GET[variable].value)
            except ValueError:
                form_values[variable] = default_value
        else:
            form_values[variable] = default_value
    return form_values
