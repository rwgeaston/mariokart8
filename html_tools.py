#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def html_table(two_d_array, sortable=False):
    strings = []
    if sortable:
        strings.append('<table class="sortable" border="1">')
    else:
        strings.append('<table border="1">')
    for row in two_d_array:
        strings.append('<tr>')
        for element in row:
            strings.extend(['<td>', str(element), '</td>'])
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


def html_wrap(tag, text, span_args=""):
    return (
        "<{tag} {args}>{text}</{tag}>"
        .format(tag=tag, text=text, args=span_args)
    )


def bold(text, span_args=""):
    return html_wrap('b', text, span_args)


def paragraph(text, span_args=""):
    return html_wrap('p', text, span_args)
