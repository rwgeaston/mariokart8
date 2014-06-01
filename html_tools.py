#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def html_table(two_d_array):
    strings = ['<table border="1">']
    for row in two_d_array:
        strings.append('<tr>')
        for element in row:
            strings.extend(['<td>', element, '</td>'])
        strings.append('</tr>')
    strings.append('</table>')
    return ''.join(strings)

def dropdown_box(name, options, default, options_friendly):
    html = ['<select name="{}">'.format(name)]
    for option, option_friendly in zip(options, options_friendly):
        if option == default:
            html.append(
                '<option selected="True" value="{}">{}</option>'
                .format(option, option_friendly)
            )
        else:
            html.append(
                '<option value="{}">{}</option>'
                .format(option, option_friendly)
            )
    html.append('</select>')
    return '\n'.join(html)